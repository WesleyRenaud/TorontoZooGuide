from __future__ import annotations

from dataclasses import replace

from ..conflicts.itinerary_schedule_time_conflicts import schedule_time_conflict_warning
from ..conflicts.itinerary_unschedule_confirmations import unschedule_confirmation_warning
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from .set_itinerary_context import build_set_itinerary_error_result
from .set_itinerary_context import SetItineraryContext
from ...shared.enums import ItineraryErrorType
from ..warnings.attraction_without_animal_warning_builder import AttractionWithoutAnimalWarningBuilder
from ..warnings.early_admission_warning_builder import EarlyAdmissionWarningBuilder
from ..warnings.fixed_time_item_long_wait_warning_builder import FixedTimeItemLongWaitWarningBuilder
from ..warnings.guardians_talk_without_animal_warning_builder import GuardiansTalkWithoutAnimalWarningBuilder
from ..warnings.itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from ..warnings.short_visit_warning_builder import ShortVisitWarningBuilder
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


def check_set_itinerary_save_warnings(
      context: SetItineraryContext,
      *,
      confirming_short_visit: bool,
      confirming_early_admission: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool,
      confirming_fixed_time_item_long_wait: bool,
      confirming_guardians_talk_without_animal: bool,
      confirming_attraction_without_animal: bool,
      overriding_conflicting_guardians_talks: bool ) -> tuple[
         SetItineraryContext,
         ItinerarySaveResult | None,
      ]:
   save_input = context.save_input
   controller_kwargs = context.itinerary_controller_kwargs
   suppressed_warnings: list[ ItineraryErrorType ] = []
   zoo_hours_record = (
      ZooHoursProvider.fetch_zoo_hours_record(
         context.conn,
         save_input.date.isoformat() )
      if save_input.arrival_time is not None
      else None )

   if (
         save_input.arrival_time is not None
         and EarlyAdmissionWarningBuilder.is_required(
            context.conn,
            save_input.arrival_time,
            zoo_hours_record,
            confirming_early_admission=confirming_early_admission,
            suppressed_warnings=suppressed_warnings )
   ):
      return (
         replace( context, suppressed_warnings=suppressed_warnings ),
         build_set_itinerary_error_result(
            context.conn,
            ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            controller_kwargs,
            suppressed_warnings=suppressed_warnings ),
      )

   if (
         save_input.arrival_time is not None
         and save_input.departure_time is not None
         and ShortVisitWarningBuilder.is_required(
            context.conn,
            save_input.arrival_time,
            save_input.departure_time,
            confirming_short_visit=confirming_short_visit,
            suppressed_warnings=suppressed_warnings )
   ):
      return (
         replace( context, suppressed_warnings=suppressed_warnings ),
         build_set_itinerary_error_result(
            context.conn,
            ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            controller_kwargs,
            suppressed_warnings=suppressed_warnings ),
      )

   updated_context = replace( context, suppressed_warnings=suppressed_warnings )

   schedule_conflict_warning = schedule_time_conflict_warning(
      context.validated_itinerary.guardians_talks,
      context.validated_itinerary.wild_encounters,
      context.current_itinerary,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )

   if schedule_conflict_warning is not None:
      return (
         updated_context,
         ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
            schedule_conflict_warning,
            suppressed_warnings ),
      )

   pending_reasons = []

   if context.saved_itinerary is not None:
      unschedule_warning = unschedule_confirmation_warning(
         context.unschedule_requirements,
         context.current_itinerary,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

      if unschedule_warning is not None:
         pending_reasons.extend( unschedule_warning.reasons )

   if GuardiansTalkWithoutAnimalWarningBuilder.is_required(
         context.validated_itinerary,
         context.conn,
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ),
         saved_itinerary=context.saved_itinerary ):
      missing_animal_talks = GuardiansTalkWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
         context.validated_itinerary,
         context.conn,
         saved_itinerary=context.saved_itinerary )
      pending_reasons.append(
         GuardiansTalkWithoutAnimalWarningBuilder.build_issue_from_talks(
            missing_animal_talks ) )

   if AttractionWithoutAnimalWarningBuilder.is_required(
         context.validated_itinerary,
         context.conn,
         confirming_attraction_without_animal=(
            confirming_attraction_without_animal ),
         saved_itinerary=context.saved_itinerary ):
      missing_animal_attractions = AttractionWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
         context.validated_itinerary,
         context.conn,
         saved_itinerary=context.saved_itinerary )
      pending_reasons.append(
         AttractionWithoutAnimalWarningBuilder.build_issue_from_attractions(
            missing_animal_attractions ) )

   if (
         not confirming_fixed_time_item_long_wait
         and not FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items(
            context.validated_itinerary )
   ):
      long_wait_reason = BulkRescheduleLongWaitSimulator.newly_added_reason(
         context.conn,
         context.validated_itinerary,
         visit_date=context.save_input.date,
         itinerary_context=context.itinerary_controller_kwargs,
         saved_itinerary=context.saved_itinerary )

      if long_wait_reason is not None:
         pending_reasons.append( long_wait_reason )

   if pending_reasons:
      return (
         updated_context,
         ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
            ItinerarySaveResult(
               status=pending_reasons[ 0 ].code,
               reasons=pending_reasons,
               itinerary=context.current_itinerary,
            ),
            suppressed_warnings ),
      )

   return ( updated_context, None )
