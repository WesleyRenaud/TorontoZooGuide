from __future__ import annotations

from dataclasses import replace

from ..conflicts.itinerary_unschedule_confirmations import apply_confirmed_itinerary_unschedule_changes
from ..conflicts.wild_encounter_time_conflicts import find_schedule_time_conflict_issues
from ..data_access.clear_itinerary_provider import ClearItineraryProvider
from ..data_access.save_itinerary_provider import SaveItineraryProvider
from .itinerary_save_context import ItinerarySaveContext
from .itinerary_save_context_builder import ItinerarySaveContextBuilder
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from ..scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from ..scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from ..scheduling.unscheduling.guardians_talk_schedule_trimmer import GuardiansTalkScheduleTrimmer
from ...shared.enums import ItineraryErrorType


class ItinerarySaveCommitter():
   @classmethod
   def commit(
         cls,
         context: ItinerarySaveContext,
         *,
         overriding_conflicting_guardians_talks: bool ) -> ItinerarySaveResult:
      validated_itinerary = context.validated_itinerary

      if overriding_conflicting_guardians_talks:
         trimmed_guardians_talks = GuardiansTalkScheduleTrimmer.apply(
            validated_itinerary.guardians_talks,
            validated_itinerary.wild_encounters )
         validated_itinerary = replace(
            validated_itinerary,
            guardians_talks=trimmed_guardians_talks )

      if context.saved_itinerary is not None:
         validated_itinerary = apply_confirmed_itinerary_unschedule_changes(
            validated_itinerary,
            context.unschedule_requirements )

      remaining_conflicts = find_schedule_time_conflict_issues(
         validated_itinerary.guardians_talks,
         validated_itinerary.wild_encounters )

      if remaining_conflicts:
         return ItinerarySaveResult(
            status=ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
            reasons=remaining_conflicts,
            suppressed_warnings=context.suppressed_warnings,
            itinerary=context.current_itinerary )

      ClearItineraryProvider.clear_itinerary( context.conn )
      SaveItineraryProvider.save_validated_itinerary(
         context.conn,
         context.save_input.date,
         validated_itinerary,
         selected_exhibits=context.save_input.selected_exhibits )

      if context.validated_itinerary.needs_schedule_reschedule:
         reschedule_result = FixedTimeActivityRescheduler.reschedule_after_add(
            context.conn,
            saved_itinerary_before_clear=context.saved_itinerary,
            **context.itinerary_controller_kwargs )
         itinerary = reschedule_result.itinerary
         ScheduledEndpointVisitTimesSyncer.seed_if_complete(
            context.conn,
            itinerary )
         ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete(
            context.conn,
            previous_itinerary=context.current_itinerary,
            current_itinerary=ItinerarySaveContextBuilder.current_itinerary(
               context.conn,
               context.itinerary_controller_kwargs ) )
         itinerary = ItinerarySaveContextBuilder.current_itinerary(
            context.conn,
            context.itinerary_controller_kwargs )
         result = ItinerarySaveResult(
            status=reschedule_result.status,
            reasons=reschedule_result.reasons,
            adjustments=context.adjustments,
            suppressed_warnings=context.suppressed_warnings,
            itinerary=itinerary )
      else:
         itinerary = ItinerarySaveContextBuilder.current_itinerary(
            context.conn,
            context.itinerary_controller_kwargs )

         ScheduledEndpointVisitTimesSyncer.seed_if_complete(
            context.conn,
            itinerary )
         ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete(
            context.conn,
            previous_itinerary=context.current_itinerary,
            current_itinerary=ItinerarySaveContextBuilder.current_itinerary(
               context.conn,
               context.itinerary_controller_kwargs ) )
         itinerary = ItinerarySaveContextBuilder.current_itinerary(
            context.conn,
            context.itinerary_controller_kwargs )
         result = ItinerarySaveResult(
            adjustments=context.adjustments,
            suppressed_warnings=context.suppressed_warnings,
            itinerary=itinerary )

      ItinerarySaveResultBuilder.persist_walk_route(
         context.conn,
         **context.itinerary_controller_kwargs )

      return result
