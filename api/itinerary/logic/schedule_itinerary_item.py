from __future__ import annotations

from typing import Any

from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_default_duration import fetch_attraction_default_duration_minutes
from ..data_access.itinerary_default_duration import fetch_enclosure_default_duration_minutes
from ..data_access.itinerary_default_duration import fetch_event_default_duration_minutes
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.schedule_itinerary_item import insert_itinerary_animal_schedule
from ..data_access.schedule_itinerary_item import insert_itinerary_attraction_schedule
from ..data_access.schedule_itinerary_item import insert_itinerary_event_schedule
from ..data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ..data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from ...guardians.controllers.guardians_controller import GuardiansController
from .itinerary import build_current_itinerary
from .itinerary_save_result import ItinerarySaveResult
from ...models.itinerary_event import ItineraryEvent
from .parse_schedule_item_request import parse_schedule_item_request
from .parse_schedule_item_request import ParsedScheduleItemRequest
from .schedule_item_not_on_itinerary_warning import apply_schedule_item_not_on_itinerary_preferences
from .schedule_item_not_on_itinerary_warning import saved_itinerary_has_schedule_item
from .schedule_item_not_on_itinerary_warning import schedule_item_not_on_itinerary_warning_is_required
from ..scheduling.find_next_available_slot import find_next_available_slot
from ..scheduling.scheduling_anchor import scheduling_anchor_minutes
from ..scheduling.scheduling_anchor import scheduling_day_end_minutes
from ..scheduling.time_block import collect_time_blocks_from_itinerary
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItineraryEventType
from ...shared.enums import ScheduleItemKind
from ...types import Connection
from ...types import Cursor
from ...types import ScheduleTimeKey
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


def _build_save_result(
      conn: Connection,
      error_type: ItineraryErrorType,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      error_type=error_type,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         animal_controller,
         attraction_controller,
         guardians_controller,
         wild_encounter_controller,
         visit_date_temp=visit_date_temp ) )


def _build_success_result(
      conn: Connection,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         animal_controller,
         attraction_controller,
         guardians_controller,
         wild_encounter_controller,
         visit_date_temp=visit_date_temp ) )


def _resolve_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> tuple[ int, int ] | ItinerarySaveResult:
   visit_date = fetch_itinerary_date( conn )

   if visit_date is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         animal_controller=animal_controller,
         attraction_controller=attraction_controller,
         guardians_controller=guardians_controller,
         wild_encounter_controller=wild_encounter_controller,
         visit_date_temp=visit_date_temp )

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )

   if zoo_hours_record is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.TIME_OUT_OF_BOUNDS,
         animal_controller=animal_controller,
         attraction_controller=attraction_controller,
         guardians_controller=guardians_controller,
         wild_encounter_controller=wild_encounter_controller,
         visit_date_temp=visit_date_temp )

   anchor_minutes = scheduling_anchor_minutes(
      zoo_hours_record,
      saved_itinerary.arrival_time )
   day_end_minutes = scheduling_day_end_minutes(
      zoo_hours_record,
      saved_itinerary.departure_time )

   return ( anchor_minutes, day_end_minutes )


def _prepare_schedule_item_on_itinerary(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      parsed: ParsedScheduleItemRequest,
      *,
      itinerary_controller_kwargs: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool,
) -> ItinerarySaveResult | None:
   apply_schedule_item_not_on_itinerary_preferences(
      conn,
      suppress_schedule_item_not_on_itinerary_warning=(
         suppress_schedule_item_not_on_itinerary_warning
      ) )

   if schedule_item_not_on_itinerary_warning_is_required(
         conn,
         saved_itinerary,
         parsed,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ) ):
      return _build_save_result(
         conn,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         **itinerary_controller_kwargs )

   return None


def _apply_itinerary_animal_schedule(
      cur: Cursor,
      *,
      species: str,
      exhibit: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
) -> bool:
   if insert_if_missing:
      inserted = insert_itinerary_animal_schedule(
         cur,
         species=species,
         exhibit=exhibit,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_animal_schedule(
      cur,
      species=species,
      exhibit=exhibit,
      start_time=start_time,
      end_time=end_time )


def _apply_itinerary_attraction_schedule(
      cur: Cursor,
      *,
      name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
) -> bool:
   if insert_if_missing:
      inserted = insert_itinerary_attraction_schedule(
         cur,
         name=name,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_attraction_schedule(
      cur,
      name=name,
      start_time=start_time,
      end_time=end_time )


def schedule_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool ) -> ItinerarySaveResult:
   itinerary_controller_kwargs = {
      'animal_controller': animal_controller,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
   }
   schedule_item_kwargs = {
      **itinerary_controller_kwargs,
      'confirming_schedule_item_not_on_itinerary': (
         confirming_schedule_item_not_on_itinerary
      ),
      'suppress_schedule_item_not_on_itinerary_warning': (
         suppress_schedule_item_not_on_itinerary_warning
      ),
   }

   parsed = parse_schedule_item_request( item_type, key )

   if parsed is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   if parsed.kind == ScheduleItemKind.ANIMAL:
      return schedule_itinerary_animal(
         conn,
         parsed,
         **schedule_item_kwargs )

   if parsed.kind == ScheduleItemKind.ATTRACTION:
      return schedule_itinerary_attraction(
         conn,
         parsed,
         **schedule_item_kwargs )

   return schedule_itinerary_event(
      conn,
      event_type=parsed.event_type,
      **itinerary_controller_kwargs )


def schedule_itinerary_animal(
      conn: Connection,
      parsed: ParsedScheduleItemRequest,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None,
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool ) -> ItinerarySaveResult:
   species = parsed.species
   exhibit = parsed.exhibit
   itinerary_controller_kwargs = {
      'animal_controller': animal_controller,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
      'visit_date_temp': visit_date_temp,
   }
   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      animal_controller=animal_controller,
      attraction_controller=attraction_controller,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
      visit_date_temp=visit_date_temp )

   if isinstance( window, ItinerarySaveResult ):
      return window

   membership_error = _prepare_schedule_item_on_itinerary(
      conn,
      saved_itinerary,
      parsed,
      itinerary_controller_kwargs=itinerary_controller_kwargs,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ),
      suppress_schedule_item_not_on_itinerary_warning=(
         suppress_schedule_item_not_on_itinerary_warning
      ) )

   if membership_error is not None:
      return membership_error

   needs_itinerary_insert = not saved_itinerary_has_schedule_item(
      saved_itinerary,
      parsed )
   anchor_minutes, day_end_minutes = window
   duration_minutes = fetch_enclosure_default_duration_minutes(
      conn,
      species,
      exhibit )

   if duration_minutes is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   itinerary = build_current_itinerary(
      saved_itinerary,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      visit_date_temp=visit_date_temp )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   slot = find_next_available_slot(
      blockers,
      anchor_minutes,
      duration_minutes,
      day_end_minutes )

   if slot is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.NO_AVAILABLE_SLOT,
         **itinerary_controller_kwargs )

   start_time, end_time = slot
   cur = conn.cursor()

   try:
      scheduled = _apply_itinerary_animal_schedule(
         cur,
         species=species,
         exhibit=exhibit,
         start_time=start_time,
         end_time=end_time,
         insert_if_missing=needs_itinerary_insert )

      if not scheduled:
         return _build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            **itinerary_controller_kwargs )

      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def schedule_itinerary_attraction(
      conn: Connection,
      parsed: ParsedScheduleItemRequest,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None,
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool ) -> ItinerarySaveResult:
   name = parsed.attraction_name
   itinerary_controller_kwargs = {
      'animal_controller': animal_controller,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
      'visit_date_temp': visit_date_temp,
   }
   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      animal_controller=animal_controller,
      attraction_controller=attraction_controller,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
      visit_date_temp=visit_date_temp )

   if isinstance( window, ItinerarySaveResult ):
      return window

   membership_error = _prepare_schedule_item_on_itinerary(
      conn,
      saved_itinerary,
      parsed,
      itinerary_controller_kwargs=itinerary_controller_kwargs,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ),
      suppress_schedule_item_not_on_itinerary_warning=(
         suppress_schedule_item_not_on_itinerary_warning
      ) )

   if membership_error is not None:
      return membership_error

   needs_itinerary_insert = not saved_itinerary_has_schedule_item(
      saved_itinerary,
      parsed )
   anchor_minutes, day_end_minutes = window
   duration_minutes = fetch_attraction_default_duration_minutes( conn, name )

   if duration_minutes is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   itinerary = build_current_itinerary(
      saved_itinerary,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      visit_date_temp=visit_date_temp )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   slot = find_next_available_slot(
      blockers,
      anchor_minutes,
      duration_minutes,
      day_end_minutes )

   if slot is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.NO_AVAILABLE_SLOT,
         **itinerary_controller_kwargs )

   start_time, end_time = slot
   cur = conn.cursor()

   try:
      scheduled = _apply_itinerary_attraction_schedule(
         cur,
         name=name,
         start_time=start_time,
         end_time=end_time,
         insert_if_missing=needs_itinerary_insert )

      if not scheduled:
         return _build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            **itinerary_controller_kwargs )

      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def schedule_itinerary_event(
      conn: Connection,
      *,
      event_type: ItineraryEventType,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   controller_kwargs = {
      'animal_controller': animal_controller,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
      'visit_date_temp': visit_date_temp,
   }
   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      animal_controller=animal_controller,
      attraction_controller=attraction_controller,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
      visit_date_temp=visit_date_temp )

   if isinstance( window, ItinerarySaveResult ):
      return window

   anchor_minutes, day_end_minutes = window
   duration_minutes = fetch_event_default_duration_minutes( conn, event_type )

   if duration_minutes is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **controller_kwargs )

   itinerary = build_current_itinerary(
      saved_itinerary,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      visit_date_temp=visit_date_temp )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   slot = find_next_available_slot(
      blockers,
      anchor_minutes,
      duration_minutes,
      day_end_minutes )

   if slot is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.NO_AVAILABLE_SLOT,
         **controller_kwargs )

   start_time, end_time = slot
   event = ItineraryEvent(
      event_type=event_type,
      start_time=start_time,
      end_time=end_time )

   cur = conn.cursor()

   try:
      insert_itinerary_event_schedule( cur, event )
      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **controller_kwargs )
