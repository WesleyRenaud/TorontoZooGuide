from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence_builder import ScheduledOccurrenceBuilder
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ..fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from ....models.wild_encounter_diff import WildEncounterDiff
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ..scheduled_activity_visit_times_coverer import ScheduledActivityVisitTimesCoverer
from ....shared.enums import ItineraryErrorType
from ....types import Types
from ..unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer
from ...warnings.wild_encounter_long_wait_warning_builder import WildEncounterLongWaitWarningBuilder
from ...warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder
from ...wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class WildEncounterItineraryItemScheduler():
   @classmethod
   def _saved_wild_encounter_exists(
         cls,
         saved_itinerary: SavedItinerary,
         wild_encounter_key: WildEncounterScheduleItemKey ) -> bool:
      return SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
         saved_itinerary,
         wild_encounter_key ) is not None


   @classmethod
   def _wild_encounter_diff_for_saved_itinerary_day(
         cls,
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

      return ScheduledOccurrenceBuilder.wild_encounter(
         wild_encounter_key.name,
         encounter )


   @classmethod
   def _insert_scheduled_wild_encounter(
         cls,
         conn: Types.Connection,
         *,
         wild_encounter_key: WildEncounterScheduleItemKey,
         wild_encounter_diff: WildEncounterDiff,
         itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult | None:
      cur = conn.cursor()

      try:
         scheduled = ScheduleItineraryItemProvider.insert_itinerary_wild_encounter(
            cur,
            wild_encounter_name=wild_encounter_key.name,
            start_time=wild_encounter_diff.start_time,
            end_time=wild_encounter_diff.end_time,
            is_deleted=wild_encounter_diff.is_deleted,
         )

         if not scheduled:
            return ItinerarySaveResultBuilder.save_result(
               conn,
               ItineraryErrorType.SAVE_FAILED,
               **itinerary_context )

         conn.commit()

      finally:
         cur.close()

      return None


   @classmethod
   def schedule(
         cls,
         conn: Types.Connection,
         wild_encounter_key: WildEncounterScheduleItemKey,
         *,
         itinerary_context: dict[ str, Any ],
         confirming_wild_encounter_unschedule: bool,
         confirming_fixed_time_item_long_wait: bool ) -> ItinerarySaveResult:
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

      if saved_itinerary.is_empty():
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      if cls._saved_wild_encounter_exists( saved_itinerary, wild_encounter_key ):
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
            **itinerary_context )

      wild_encounter_diff = cls._wild_encounter_diff_for_saved_itinerary_day(
         saved_itinerary,
         wild_encounter_key,
         itinerary_context[ 'wild_encounter_coordinator' ] )

      if wild_encounter_diff.is_deleted:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE,
            **itinerary_context )

      has_overlap = WildEncounterUnschedulePreparer.saved_itinerary_has_overlap(
         saved_itinerary,
         [ wild_encounter_diff ] )

      pending_reasons: list[ ItineraryResultReason ] = []

      if has_overlap and not confirming_wild_encounter_unschedule:
         pending_reasons.append(
            WildEncounterUnscheduleWarningBuilder.build_issue( [ wild_encounter_diff ] ) )

      if not confirming_fixed_time_item_long_wait:
         long_wait_reason = (
            WildEncounterLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
               conn,
               wild_encounter_diff,
               itinerary_context=itinerary_context )
         )

         if long_wait_reason is not None:
            pending_reasons.append( long_wait_reason )

      if pending_reasons:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            pending_reasons[ 0 ].code,
            reasons=pending_reasons,
            **itinerary_context )

      insert_error = cls._insert_scheduled_wild_encounter(
         conn,
         wild_encounter_key=wild_encounter_key,
         wild_encounter_diff=wild_encounter_diff,
         itinerary_context=itinerary_context )

      if insert_error is not None:
         return insert_error

      ScheduledActivityVisitTimesCoverer.cover_for_activity(
         conn,
         start_time=wild_encounter_diff.start_time,
         end_time=wild_encounter_diff.end_time,
         current_arrival_time=saved_itinerary.arrival_time,
         current_departure_time=saved_itinerary.departure_time,
         itinerary_context=itinerary_context )

      if has_overlap and confirming_wild_encounter_unschedule:
         return FixedTimeActivityRescheduler.reschedule_after_add(
            conn,
            saved_itinerary_before_clear=saved_itinerary,
            **itinerary_context )

      ItinerarySaveResultBuilder.persist_walk_route( conn, **itinerary_context )

      return ItinerarySaveResultBuilder.success_result( conn, **itinerary_context )
