from __future__ import annotations

from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_default_duration import fetch_event_default_duration_seconds
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.schedule_itinerary_item import insert_itinerary_event_schedule
from ..data_access.schedule_itinerary_item import insert_itinerary_guardians_talk
from ..data_access.schedule_itinerary_item import insert_itinerary_wild_encounter
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .guardians_talk_unschedule_items import clear_saved_schedules_overlapping_guardians_talks
from .guardians_talk_unschedule_items import saved_itinerary_has_overlap_with_guardians_talks
from .guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue
from .itinerary_save_result import ItinerarySaveResult
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.itinerary_event import ItineraryEvent
from ...models.wild_encounter_diff import WildEncounterDiff
from .parse_schedule_item_request import parse_schedule_item_request
from .parse_schedule_time_options import parse_schedule_time_options
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from .schedule_itinerary_helpers import build_itinerary_context
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import resolve_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times
from .schedule_listed_itinerary_item import schedule_listed_itinerary_item
from ..scheduling.scheduled_occurrence import schedule_guardians_talk_for_itinerary
from ..scheduling.scheduled_occurrence import schedule_wild_encounter_for_itinerary
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
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def _schedule_itinerary_event(
      conn: Connection,
      *,
      event_type: ItineraryEventType,
      time_options: ParsedScheduleTimeOptions,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   window = resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( window, ItinerarySaveResult ):
      return window

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      fetch_event_default_duration_seconds( conn, event_type ) )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   slot, slot_error = resolve_slot_times(
      conn,
      saved_itinerary,
      window,
      duration_seconds,
      start_time=time_options.start_time,
      itinerary_context=itinerary_context )

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

   return build_success_result( conn, **itinerary_context )


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
      guardians_coordinator: type[ GuardiansCoordinator ] ) -> GuardiansTalkDiff:
   talk = guardians_coordinator.get_guardians_talk_on_day_schedule(
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
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
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
         return build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      conn.commit()

   finally:
      cur.close()

   return build_success_result( conn, **itinerary_context )


def _schedule_guardians_talk_itinerary_item(
      conn: Connection,
      talk_name: str,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_guardians_talk_unschedule: bool ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   if _saved_guardians_talk_exists( saved_itinerary, talk_name ):
      return build_success_result( conn, **itinerary_context )

   guardians_talk_diff = _guardians_talk_diff_for_saved_itinerary_day(
      saved_itinerary,
      talk_name,
      itinerary_context[ 'guardians_coordinator' ] )

   has_overlap = saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary,
      [ guardians_talk_diff ] )

   if has_overlap and not confirming_guardians_talk_unschedule:
      return build_save_result(
         conn,
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_guardians_talk_unschedule_issue( [ guardians_talk_diff ] ),
         ),
         **itinerary_context )

   return _insert_scheduled_guardians_talk(
      conn,
      saved_itinerary=saved_itinerary,
      talk_name=talk_name,
      guardians_talk_diff=guardians_talk_diff,
      clear_overlapping_schedules=(
         has_overlap and confirming_guardians_talk_unschedule ),
      itinerary_context=itinerary_context )


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
      wild_encounter_coordinator: type[ WildEncounterCoordinator ] ) -> WildEncounterDiff:
   encounter = wild_encounter_coordinator.get_wild_encounter_on_day_schedule(
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
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
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
         return build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      conn.commit()

   finally:
      cur.close()

   return build_success_result( conn, **itinerary_context )


def _schedule_wild_encounter_itinerary_item(
      conn: Connection,
      wild_encounter_name: str,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   if _saved_wild_encounter_exists( saved_itinerary, wild_encounter_name ):
      return build_success_result( conn, **itinerary_context )

   wild_encounter_diff = _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary,
      wild_encounter_name,
      itinerary_context[ 'wild_encounter_coordinator' ] )

   if wild_encounter_diff.is_deleted:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   has_overlap = saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary,
      [ wild_encounter_diff ] )

   if has_overlap and not confirming_wild_encounter_unschedule:
      return build_save_result(
         conn,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_wild_encounter_unschedule_issue( [ wild_encounter_diff ] ),
         ),
         **itinerary_context )

   return _insert_scheduled_wild_encounter(
      conn,
      saved_itinerary=saved_itinerary,
      wild_encounter_name=wild_encounter_name,
      wild_encounter_diff=wild_encounter_diff,
      clear_overlapping_schedules=(
         has_overlap and confirming_wild_encounter_unschedule ),
      itinerary_context=itinerary_context )


def schedule_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str,
      *,
      start_time: TimeInput = None,
      duration_minutes: DurationInput = None,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      confirming_schedule_item_not_on_itinerary: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator )

   parsed = parse_schedule_item_request( item_type, key )

   if parsed is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   parsed_schedule_options = parse_schedule_time_options(
      start_time,
      duration_minutes )

   if isinstance( parsed_schedule_options, ItineraryErrorType ):
      return build_save_result(
         conn,
         parsed_schedule_options,
         **itinerary_context )

   if parsed.kind == ScheduleItemKind.EVENT:
      return _schedule_itinerary_event(
         conn,
         event_type=parsed.event_type,
         time_options=parsed_schedule_options,
         itinerary_context=itinerary_context )

   if parsed.kind == ScheduleItemKind.GUARDIANS_TALK:
      return _schedule_guardians_talk_itinerary_item(
         conn,
         parsed.talk_name or '',
         itinerary_context=itinerary_context,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ) )

   if parsed.kind == ScheduleItemKind.WILD_ENCOUNTER:
      return _schedule_wild_encounter_itinerary_item(
         conn,
         parsed.wild_encounter_name or '',
         itinerary_context=itinerary_context,
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

   return schedule_listed_itinerary_item(
      conn,
      parsed,
      parsed_schedule_options,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )
