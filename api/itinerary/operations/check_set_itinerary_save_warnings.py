from __future__ import annotations

from dataclasses import replace

from ..conflicts.itinerary_schedule_time_conflicts import schedule_time_conflict_warning
from ..conflicts.itinerary_unschedule_confirmations import unschedule_confirmation_warning
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.bulk.simulate_bulk_reschedule_for_long_wait import newly_added_guardians_talks_with_long_waits
from .set_itinerary_context import build_set_itinerary_error_result
from .set_itinerary_context import SetItineraryContext
from ...shared.enums import ItineraryErrorType
from ..warnings.early_admission_warning import early_admission_warning_is_required
from ..warnings.guardians_talk_long_wait_warning import build_guardians_talk_long_wait_issue_from_talks
from ..warnings.guardians_talk_long_wait_warning import guardians_talk_long_wait_warning_is_required_for_validated_itinerary
from ..warnings.guardians_talk_without_animal_warning import build_guardians_talk_without_animal_issue_from_talks
from ..warnings.guardians_talk_without_animal_warning import guardians_talk_without_animal_warning_is_required
from ..warnings.guardians_talk_without_animal_warning import newly_added_guardians_talks_without_matching_animal
from ..warnings.itinerary_suppressed_warnings import with_suppressed_warnings
from ..warnings.short_visit_warning import short_visit_warning_is_required
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


def check_set_itinerary_save_warnings(
      context: SetItineraryContext,
      *,
      confirming_short_visit: bool,
      confirming_early_admission: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool,
      confirming_guardians_talk_long_wait: bool,
      confirming_guardians_talk_without_animal: bool,
      overriding_conflicting_guardians_talks: bool ) -> tuple[
         SetItineraryContext,
         ItinerarySaveResult | None,
      ]:
   save_input = context.save_input
   controller_kwargs = context.itinerary_controller_kwargs
   suppressed_warnings: list[ ItineraryErrorType ] = []
   zoo_hours_record = (
      fetch_zoo_hours_record(
         context.conn,
         save_input.date.isoformat() )
      if save_input.arrival_time is not None
      else None )

   if (
         save_input.arrival_time is not None
         and early_admission_warning_is_required(
            context.conn,
            save_input.arrival_time,
            zoo_hours_record,
            confirming_early_admission=confirming_early_admission,
            suppressed_warnings=suppressed_warnings )
   ):
      warning_tuple = tuple( suppressed_warnings )
      return (
         replace( context, suppressed_warnings=warning_tuple ),
         build_set_itinerary_error_result(
            context.conn,
            ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            controller_kwargs,
            suppressed_warnings=warning_tuple ),
      )

   if (
         save_input.arrival_time is not None
         and save_input.departure_time is not None
         and short_visit_warning_is_required(
            context.conn,
            save_input.arrival_time,
            save_input.departure_time,
            confirming_short_visit=confirming_short_visit,
            suppressed_warnings=suppressed_warnings )
   ):
      warning_tuple = tuple( suppressed_warnings )
      return (
         replace( context, suppressed_warnings=warning_tuple ),
         build_set_itinerary_error_result(
            context.conn,
            ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            controller_kwargs,
            suppressed_warnings=warning_tuple ),
      )

   warning_tuple = tuple( suppressed_warnings )
   updated_context = replace( context, suppressed_warnings=warning_tuple )

   schedule_conflict_warning = schedule_time_conflict_warning(
      context.validated_itinerary.guardians_talks,
      context.validated_itinerary.wild_encounters,
      context.current_itinerary,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )

   if schedule_conflict_warning is not None:
      return (
         updated_context,
         with_suppressed_warnings( schedule_conflict_warning, warning_tuple ),
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

   if guardians_talk_without_animal_warning_is_required(
         context.validated_itinerary,
         context.conn,
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ),
         saved_itinerary=context.saved_itinerary ):
      missing_animal_talks = newly_added_guardians_talks_without_matching_animal(
         context.validated_itinerary,
         context.conn,
         saved_itinerary=context.saved_itinerary )
      pending_reasons.append(
         build_guardians_talk_without_animal_issue_from_talks(
            missing_animal_talks ) )

   if guardians_talk_long_wait_warning_is_required_for_validated_itinerary(
         context.validated_itinerary,
         confirming_guardians_talk_long_wait=(
            confirming_guardians_talk_long_wait ),
         saved_itinerary=context.saved_itinerary ):
      long_wait_talks = newly_added_guardians_talks_with_long_waits(
         context.conn,
         context.validated_itinerary,
         visit_date=context.save_input.date,
         itinerary_context=context.itinerary_controller_kwargs,
         saved_itinerary=context.saved_itinerary )

      if long_wait_talks:
         pending_reasons.append(
            build_guardians_talk_long_wait_issue_from_talks(
               long_wait_talks ) )

   if pending_reasons:
      return (
         updated_context,
         with_suppressed_warnings(
            ItinerarySaveResult(
               status=pending_reasons[ 0 ].code,
               reasons=tuple( pending_reasons ),
               itinerary=context.current_itinerary,
            ),
            warning_tuple ),
      )

   return ( updated_context, None )
