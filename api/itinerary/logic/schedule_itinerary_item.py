from __future__ import annotations

from collections.abc import Callable
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
from ..data_access.schedule_itinerary_item import insert_itinerary_guardians_talk
from ..data_access.schedule_itinerary_item import insert_itinerary_wild_encounter
from ..data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ..data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from ...guardians.controllers.guardians_controller import GuardiansController
from .guardians_talk_unschedule_items import clear_saved_schedules_overlapping_guardians_talks
from .guardians_talk_unschedule_items import saved_itinerary_has_overlap_with_guardians_talks
from .guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue
from .itinerary import build_current_itinerary
from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_result import ItinerarySaveResult
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.itinerary_event import ItineraryEvent
from ...models.wild_encounter_diff import WildEncounterDiff
from .parse_schedule_item_request import parse_schedule_item_request
from .parse_schedule_item_request import ParsedScheduleItemRequest
from .parse_schedule_time_options import parse_schedule_time_options
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from .schedule_item_not_on_itinerary_warning import apply_schedule_item_not_on_itinerary_preferences
from .schedule_item_not_on_itinerary_warning import saved_itinerary_has_schedule_item
from .schedule_item_not_on_itinerary_warning import schedule_item_not_on_itinerary_warning_is_required
from ..scheduling.resolve_schedule_slot import resolve_schedule_slot
from ..scheduling.scheduled_occurrence import schedule_guardians_talk_for_itinerary
from ..scheduling.scheduled_occurrence import schedule_wild_encounter_for_itinerary
from ..scheduling.scheduling_anchor import scheduling_anchor_minutes
from ..scheduling.scheduling_anchor import scheduling_day_end_minutes
from ..scheduling.time_block import collect_time_blocks_from_itinerary
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItineraryEventType
from ...shared.enums import ScheduleItemKind
from ...types import Connection
from ...types import Cursor
from ...types import DurationInput
from ...types import ScheduleTimeKey
from ...types import TimeInput
from .wild_encounter_unschedule_items import clear_saved_schedules_overlapping_wild_encounters
from .wild_encounter_unschedule_items import saved_itinerary_has_overlap_with_wild_encounters
from .wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


def _itinerary_controller_kwargs(
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> dict[ str, Any ]:
   return {
      'animal_controller': animal_controller,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
      'visit_date_temp': visit_date_temp,
   }


def _build_save_result(
      conn: Connection,
      error_type: ItineraryErrorType,
      *,
      issues: tuple[ ItinerarySaveIssue, ... ] = (),
      **itinerary_controller_kwargs: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      error_type=error_type,
      issues=issues,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_controller_kwargs ) )


def _build_success_result(
      conn: Connection,
      **itinerary_controller_kwargs: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_controller_kwargs ) )


def _resolve_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      **itinerary_controller_kwargs: Any ) -> tuple[ int, int ] | ItinerarySaveResult:
   visit_date = fetch_itinerary_date( conn )

   if visit_date is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_controller_kwargs )

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )

   if zoo_hours_record is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.TIME_OUT_OF_BOUNDS,
         **itinerary_controller_kwargs )

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


def _resolve_slot_times(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      window: tuple[ int, int ],
      duration_minutes: int,
      *,
      start_time: ScheduleTimeKey | None,
      itinerary_controller_kwargs: dict[ str, Any ],
) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
   anchor_minutes, day_end_minutes = window
   itinerary = build_current_itinerary( saved_itinerary, **itinerary_controller_kwargs )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   slot = resolve_schedule_slot(
      blockers,
      anchor_minutes,
      duration_minutes,
      day_end_minutes,
      start_time=start_time )

   if slot is None:
      error_type = (
         ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE
         if start_time is not None
         else ItineraryErrorType.NO_AVAILABLE_SLOT )

      return None, _build_save_result(
         conn,
         error_type,
         **itinerary_controller_kwargs )

   return slot, None


def _effective_duration_minutes(
      duration_minutes: int | None,
      default_duration_minutes: int | None ) -> int | None:
   if default_duration_minutes is None:
      return None

   if duration_minutes is not None:
      return duration_minutes

   return default_duration_minutes


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


def _commit_listed_schedule(
      conn: Connection,
      *,
      apply_schedule: Callable[
         [ Cursor, ScheduleTimeKey, ScheduleTimeKey, bool ],
         bool,
      ],
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      itinerary_controller_kwargs: dict[ str, Any ],
) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      scheduled = apply_schedule(
         cur,
         start_time,
         end_time,
         insert_if_missing )

      if not scheduled:
         return _build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            **itinerary_controller_kwargs )

      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def _schedule_listed_itinerary_item(
      conn: Connection,
      parsed: ParsedScheduleItemRequest,
      time_options: ParsedScheduleTimeOptions,
      *,
      itinerary_controller_kwargs: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool,
) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_controller_kwargs )

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

   if parsed.kind == ScheduleItemKind.ANIMAL:
      default_duration_minutes = fetch_enclosure_default_duration_minutes(
         conn,
         parsed.species,
         parsed.exhibit )

      def apply_schedule(
            cur: Cursor,
            start_time: ScheduleTimeKey,
            end_time: ScheduleTimeKey,
            insert_if_missing: bool ) -> bool:
         return _apply_itinerary_animal_schedule(
            cur,
            species=parsed.species,
            exhibit=parsed.exhibit,
            start_time=start_time,
            end_time=end_time,
            insert_if_missing=insert_if_missing )

   else:
      default_duration_minutes = fetch_attraction_default_duration_minutes(
         conn,
         parsed.attraction_name )

      def apply_schedule(
            cur: Cursor,
            start_time: ScheduleTimeKey,
            end_time: ScheduleTimeKey,
            insert_if_missing: bool ) -> bool:
         return _apply_itinerary_attraction_schedule(
            cur,
            name=parsed.attraction_name,
            start_time=start_time,
            end_time=end_time,
            insert_if_missing=insert_if_missing )

   effective_duration = _effective_duration_minutes(
      time_options.duration_minutes,
      default_duration_minutes )

   if effective_duration is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   slot, slot_error = _resolve_slot_times(
      conn,
      saved_itinerary,
      window,
      effective_duration,
      start_time=time_options.start_time,
      itinerary_controller_kwargs=itinerary_controller_kwargs )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot

   return _commit_listed_schedule(
      conn,
      apply_schedule=apply_schedule,
      start_time=start_time_key,
      end_time=end_time,
      insert_if_missing=not saved_itinerary_has_schedule_item( saved_itinerary, parsed ),
      itinerary_controller_kwargs=itinerary_controller_kwargs )


def _schedule_itinerary_event(
      conn: Connection,
      *,
      event_type: ItineraryEventType,
      time_options: ParsedScheduleTimeOptions,
      itinerary_controller_kwargs: dict[ str, Any ],
) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_controller_kwargs )

   if isinstance( window, ItinerarySaveResult ):
      return window

   effective_duration = _effective_duration_minutes(
      time_options.duration_minutes,
      fetch_event_default_duration_minutes( conn, event_type ) )

   if effective_duration is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   slot, slot_error = _resolve_slot_times(
      conn,
      saved_itinerary,
      window,
      effective_duration,
      start_time=time_options.start_time,
      itinerary_controller_kwargs=itinerary_controller_kwargs )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot
   event = ItineraryEvent(
      event_type=event_type,
      start_time=start_time_key,
      end_time=end_time )

   cur = conn.cursor()

   try:
      insert_itinerary_event_schedule( cur, event )
      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def _saved_guardians_talk_exists(
      saved_itinerary: SavedItinerary,
      talk_name: str ) -> bool:
   return any(
      row.talk_name == talk_name and not row.is_deleted
      for row in saved_itinerary.guardians_talk_rows
   )


def _guardians_talk_diff_for_saved_itinerary_day(
      saved_itinerary: SavedItinerary,
      talk_name: str,
      guardians_controller: type[ GuardiansController ],
) -> GuardiansTalkDiff:
   talk = guardians_controller.get_guardians_talk_on_day_schedule(
      month=saved_itinerary.month(),
      day=saved_itinerary.day(),
      year=saved_itinerary.year(),
      talk_name=talk_name )

   return schedule_guardians_talk_for_itinerary( talk_name, talk )


def _insert_scheduled_guardians_talk(
      conn: Connection,
      *,
      saved_itinerary: SavedItinerary,
      talk_name: str,
      guardians_talk_diff: GuardiansTalkDiff,
      clear_overlapping_schedules: bool,
      itinerary_controller_kwargs: dict[ str, Any ],
) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      if clear_overlapping_schedules:
         clear_saved_schedules_overlapping_guardians_talks(
            cur,
            saved_itinerary,
            [ guardians_talk_diff ] )

      scheduled = insert_itinerary_guardians_talk(
         cur,
         talk_name=talk_name,
         start_time=guardians_talk_diff.start_time,
         end_time=guardians_talk_diff.end_time,
      )

      if not scheduled:
         return _build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_controller_kwargs )

      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def _schedule_guardians_talk_itinerary_item(
      conn: Connection,
      talk_name: str,
      *,
      itinerary_controller_kwargs: dict[ str, Any ],
      confirming_guardians_talk_unschedule: bool,
) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return _build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_controller_kwargs )

   if _saved_guardians_talk_exists( saved_itinerary, talk_name ):
      return _build_success_result( conn, **itinerary_controller_kwargs )

   guardians_talk_diff = _guardians_talk_diff_for_saved_itinerary_day(
      saved_itinerary,
      talk_name,
      itinerary_controller_kwargs[ 'guardians_controller' ] )

   has_overlap = saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary,
      [ guardians_talk_diff ] )

   if has_overlap and not confirming_guardians_talk_unschedule:
      return _build_save_result(
         conn,
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         issues=(
            build_guardians_talk_unschedule_issue( [ guardians_talk_diff ] ),
         ),
         **itinerary_controller_kwargs )

   return _insert_scheduled_guardians_talk(
      conn,
      saved_itinerary=saved_itinerary,
      talk_name=talk_name,
      guardians_talk_diff=guardians_talk_diff,
      clear_overlapping_schedules=(
         has_overlap and confirming_guardians_talk_unschedule ),
      itinerary_controller_kwargs=itinerary_controller_kwargs )


def _saved_wild_encounter_exists(
      saved_itinerary: SavedItinerary,
      wild_encounter_name: str ) -> bool:
   return any(
      row.wild_encounter == wild_encounter_name and not row.is_deleted
      for row in saved_itinerary.wild_encounter_rows
   )


def _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary: SavedItinerary,
      wild_encounter_name: str,
      wild_encounter_controller: type[ WildEncounterController ],
) -> WildEncounterDiff:
   encounter = wild_encounter_controller.get_wild_encounter_on_day_schedule(
      month=saved_itinerary.month(),
      day=saved_itinerary.day(),
      year=saved_itinerary.year(),
      encounter_name=wild_encounter_name )

   return schedule_wild_encounter_for_itinerary( wild_encounter_name, encounter )


def _insert_scheduled_wild_encounter(
      conn: Connection,
      *,
      saved_itinerary: SavedItinerary,
      wild_encounter_name: str,
      wild_encounter_diff: WildEncounterDiff,
      clear_overlapping_schedules: bool,
      itinerary_controller_kwargs: dict[ str, Any ],
) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      if clear_overlapping_schedules:
         clear_saved_schedules_overlapping_wild_encounters(
            cur,
            saved_itinerary,
            [ wild_encounter_diff ] )

      scheduled = insert_itinerary_wild_encounter(
         cur,
         wild_encounter_name=wild_encounter_name,
         start_time=wild_encounter_diff.start_time,
         end_time=wild_encounter_diff.end_time,
         is_deleted=wild_encounter_diff.is_deleted,
      )

      if not scheduled:
         return _build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_controller_kwargs )

      conn.commit()

   finally:
      cur.close()

   return _build_success_result( conn, **itinerary_controller_kwargs )


def _schedule_wild_encounter_itinerary_item(
      conn: Connection,
      wild_encounter_name: str,
      *,
      itinerary_controller_kwargs: dict[ str, Any ],
      confirming_wild_encounter_unschedule: bool,
) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return _build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_controller_kwargs )

   if _saved_wild_encounter_exists( saved_itinerary, wild_encounter_name ):
      return _build_success_result( conn, **itinerary_controller_kwargs )

   wild_encounter_diff = _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary,
      wild_encounter_name,
      itinerary_controller_kwargs[ 'wild_encounter_controller' ] )

   if wild_encounter_diff.is_deleted:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   has_overlap = saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary,
      [ wild_encounter_diff ] )

   if has_overlap and not confirming_wild_encounter_unschedule:
      return _build_save_result(
         conn,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         issues=(
            build_wild_encounter_unschedule_issue( [ wild_encounter_diff ] ),
         ),
         **itinerary_controller_kwargs )

   return _insert_scheduled_wild_encounter(
      conn,
      saved_itinerary=saved_itinerary,
      wild_encounter_name=wild_encounter_name,
      wild_encounter_diff=wild_encounter_diff,
      clear_overlapping_schedules=(
         has_overlap and confirming_wild_encounter_unschedule ),
      itinerary_controller_kwargs=itinerary_controller_kwargs )


def schedule_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str,
      *,
      start_time: TimeInput = None,
      duration_minutes: DurationInput = None,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      confirming_schedule_item_not_on_itinerary: bool,
      suppress_schedule_item_not_on_itinerary_warning: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   itinerary_controller_kwargs = _itinerary_controller_kwargs(
      animal_controller=animal_controller,
      attraction_controller=attraction_controller,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller )

   parsed = parse_schedule_item_request( item_type, key )

   if parsed is None:
      return _build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_controller_kwargs )

   parsed_schedule_options = parse_schedule_time_options(
      start_time,
      duration_minutes )

   if isinstance( parsed_schedule_options, ItineraryErrorType ):
      return _build_save_result(
         conn,
         parsed_schedule_options,
         **itinerary_controller_kwargs )

   if parsed.kind == ScheduleItemKind.EVENT:
      return _schedule_itinerary_event(
         conn,
         event_type=parsed.event_type,
         time_options=parsed_schedule_options,
         itinerary_controller_kwargs=itinerary_controller_kwargs )

   if parsed.kind == ScheduleItemKind.GUARDIANS_TALK:
      return _schedule_guardians_talk_itinerary_item(
         conn,
         parsed.talk_name or '',
         itinerary_controller_kwargs=itinerary_controller_kwargs,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ) )

   if parsed.kind == ScheduleItemKind.WILD_ENCOUNTER:
      return _schedule_wild_encounter_itinerary_item(
         conn,
         parsed.wild_encounter_name or '',
         itinerary_controller_kwargs=itinerary_controller_kwargs,
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

   return _schedule_listed_itinerary_item(
      conn,
      parsed,
      parsed_schedule_options,
      itinerary_controller_kwargs=itinerary_controller_kwargs,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ),
      suppress_schedule_item_not_on_itinerary_warning=(
         suppress_schedule_item_not_on_itinerary_warning
      ) )
