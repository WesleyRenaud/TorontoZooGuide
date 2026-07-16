from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence import schedule_wild_encounter_for_itinerary
from ...data_access.find_saved_itinerary_schedule_item_row import find_saved_itinerary_schedule_item_row
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_wild_encounter
from ..extend_departure_for_activity import cover_visit_times_for_scheduled_activity
from ....models.wild_encounter_diff import WildEncounterDiff
from ..reschedule_itinerary_item_schedules import reschedule_itinerary_items_after_fixed_time_activity_add
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import persist_itinerary_walk_route
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.wild_encounter_unschedule_items import saved_itinerary_has_overlap_with_wild_encounters
from ...warnings.wild_encounter_long_wait_warning import wild_encounter_long_wait_reason_after_adding_with_simulated_bulk
from ...warnings.wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from ...wild_encounter_item_key import WildEncounterScheduleItemKey
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def _saved_wild_encounter_exists(
      saved_itinerary: SavedItinerary,
      wild_encounter_key: WildEncounterScheduleItemKey ) -> bool:
   return find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      wild_encounter_key ) is not None


def _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary: SavedItinerary,
      wild_encounter_key: WildEncounterScheduleItemKey,
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
   ) -> WildEncounterDiff:
   encounter = wild_encounter_coordinator.get_wild_encounter_on_day_schedule(
      month=saved_itinerary.month(),
      day=saved_itinerary.day(),
      year=saved_itinerary.year(),
      encounter_name=wild_encounter_key.name,
      start_time=wild_encounter_key.start_time )

   return schedule_wild_encounter_for_itinerary(
      wild_encounter_key.name,
      encounter )


def _insert_scheduled_wild_encounter(
      conn: Connection,
      *,
      wild_encounter_key: WildEncounterScheduleItemKey,
      wild_encounter_diff: WildEncounterDiff,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult | None:
   cur = conn.cursor()

   try:
      scheduled = insert_itinerary_wild_encounter(
         cur,
         wild_encounter_name=wild_encounter_key.name,
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

   return None


def schedule_wild_encounter_itinerary_item(
      conn: Connection,
      wild_encounter_key: WildEncounterScheduleItemKey,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_wild_encounter_unschedule: bool,
      confirming_fixed_time_item_long_wait: bool ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   if _saved_wild_encounter_exists( saved_itinerary, wild_encounter_key ):
      return build_save_result(
         conn,
         ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
         **itinerary_context )

   wild_encounter_diff = _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary,
      wild_encounter_key,
      itinerary_context[ 'wild_encounter_coordinator' ] )

   if wild_encounter_diff.is_deleted:
      return build_save_result(
         conn,
         ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE,
         **itinerary_context )

   has_overlap = saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary,
      [ wild_encounter_diff ] )

   pending_reasons: list[ ItineraryResultReason ] = []

   if has_overlap and not confirming_wild_encounter_unschedule:
      pending_reasons.append(
         build_wild_encounter_unschedule_issue( [ wild_encounter_diff ] ) )

   if not confirming_fixed_time_item_long_wait:
      long_wait_reason = (
         wild_encounter_long_wait_reason_after_adding_with_simulated_bulk(
            conn,
            wild_encounter_diff,
            itinerary_context=itinerary_context )
      )

      if long_wait_reason is not None:
         pending_reasons.append( long_wait_reason )

   if pending_reasons:
      return build_save_result(
         conn,
         pending_reasons[ 0 ].code,
         reasons=tuple( pending_reasons ),
         **itinerary_context )

   insert_error = _insert_scheduled_wild_encounter(
      conn,
      wild_encounter_key=wild_encounter_key,
      wild_encounter_diff=wild_encounter_diff,
      itinerary_context=itinerary_context )

   if insert_error is not None:
      return insert_error

   cover_visit_times_for_scheduled_activity(
      conn,
      start_time=wild_encounter_diff.start_time,
      end_time=wild_encounter_diff.end_time,
      current_arrival_time=saved_itinerary.arrival_time,
      current_departure_time=saved_itinerary.departure_time,
      itinerary_context=itinerary_context )

   if has_overlap and confirming_wild_encounter_unschedule:
      return reschedule_itinerary_items_after_fixed_time_activity_add(
         conn,
         saved_itinerary_before_clear=saved_itinerary,
         **itinerary_context )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
