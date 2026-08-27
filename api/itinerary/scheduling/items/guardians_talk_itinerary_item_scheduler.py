from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence_builder import ScheduledOccurrenceBuilder
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ..fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...guardians_talk_item_key import GuardiansTalkScheduleItemKey
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ..scheduled_activity_visit_times_coverer import ScheduledActivityVisitTimesCoverer
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from ...warnings.guardians_talk_long_wait_warning_builder import GuardiansTalkLongWaitWarningBuilder
from ...warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from ...warnings.guardians_talk_without_animal_warning_builder import GuardiansTalkWithoutAnimalWarningBuilder


class GuardiansTalkItineraryItemScheduler():
   @classmethod
   def _saved_guardians_talk_exists(
         cls,
         saved_itinerary: SavedItinerary,
         guardians_talk_key: GuardiansTalkScheduleItemKey ) -> bool:
      return SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
         saved_itinerary,
         guardians_talk_key ) is not None


   @classmethod
   def _guardians_talk_diff_for_saved_itinerary_day(
         cls,
         saved_itinerary: SavedItinerary,
         guardians_talk_key: GuardiansTalkScheduleItemKey,
         guardians_coordinator: type[ GuardiansCoordinator ] ) -> GuardiansTalkDiff:
      talk = guardians_coordinator.get_guardians_talk_on_day_schedule(
         month=saved_itinerary.month(),
         day=saved_itinerary.day(),
         year=saved_itinerary.year(),
         talk_name=guardians_talk_key.name,
         start_time=guardians_talk_key.start_time )

      return ScheduledOccurrenceBuilder.guardians_talk(
         guardians_talk_key.name,
         talk )


   @classmethod
   def _insert_scheduled_guardians_talk(
         cls,
         conn: Connection,
         *,
         guardians_talk_key: GuardiansTalkScheduleItemKey,
         guardians_talk_diff: GuardiansTalkDiff,
         itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult | None:
      cur = conn.cursor()

      try:
         scheduled = ScheduleItineraryItemProvider.insert_itinerary_guardians_talk(
            cur,
            talk_name=guardians_talk_key.name,
            start_time=guardians_talk_diff.start_time,
            end_time=guardians_talk_diff.end_time,
            is_deleted=guardians_talk_diff.is_deleted,
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
         conn: Connection,
         guardians_talk_key: GuardiansTalkScheduleItemKey,
         *,
         itinerary_context: dict[ str, Any ],
         confirming_guardians_talk_unschedule: bool,
         confirming_fixed_time_item_long_wait: bool,
         confirming_guardians_talk_without_animal: bool ) -> ItinerarySaveResult:
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

      if saved_itinerary.is_empty():
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      if cls._saved_guardians_talk_exists( saved_itinerary, guardians_talk_key ):
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
            **itinerary_context )

      guardians_talk_diff = cls._guardians_talk_diff_for_saved_itinerary_day(
         saved_itinerary,
         guardians_talk_key,
         itinerary_context[ 'guardians_coordinator' ] )

      if guardians_talk_diff.is_deleted:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE,
            **itinerary_context )

      has_overlap = GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap(
         saved_itinerary,
         [ guardians_talk_diff ] )

      pending_reasons: list[ ItineraryResultReason ] = []

      if has_overlap and not confirming_guardians_talk_unschedule:
         pending_reasons.append(
            GuardiansTalkUnscheduleWarningBuilder.build_issue( [ guardians_talk_diff ] ) )

      if GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk(
            guardians_talk_diff,
            saved_itinerary.species_exhibit_pairs(),
            conn,
            confirming_guardians_talk_without_animal=(
               confirming_guardians_talk_without_animal ) ):
         pending_reasons.append(
            GuardiansTalkWithoutAnimalWarningBuilder.build_issue_from_talks(
               [ guardians_talk_diff ] ) )

      if not confirming_fixed_time_item_long_wait:
         long_wait_reason = (
            GuardiansTalkLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
               conn,
               guardians_talk_diff,
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

      insert_error = cls._insert_scheduled_guardians_talk(
         conn,
         guardians_talk_key=guardians_talk_key,
         guardians_talk_diff=guardians_talk_diff,
         itinerary_context=itinerary_context )

      if insert_error is not None:
         return insert_error

      ScheduledActivityVisitTimesCoverer.cover_for_activity(
         conn,
         start_time=guardians_talk_diff.start_time,
         end_time=guardians_talk_diff.end_time,
         current_arrival_time=saved_itinerary.arrival_time,
         current_departure_time=saved_itinerary.departure_time,
         itinerary_context=itinerary_context )

      if has_overlap and confirming_guardians_talk_unschedule:
         return FixedTimeActivityRescheduler.reschedule_after_add(
            conn,
            saved_itinerary_before_clear=saved_itinerary,
            **itinerary_context )

      ItinerarySaveResultBuilder.persist_walk_route( conn, **itinerary_context )

      return ItinerarySaveResultBuilder.success_result( conn, **itinerary_context )
