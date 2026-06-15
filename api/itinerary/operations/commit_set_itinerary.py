from __future__ import annotations

from dataclasses import replace

from ..conflicts.itinerary_unschedule_confirmations import apply_confirmed_itinerary_unschedule_changes
from ..conflicts.wild_encounter_time_conflicts import find_schedule_time_conflict_issues
from ..data_access.clear_itinerary import clear_itinerary
from ..data_access.save_itinerary import save_validated_itinerary
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.unscheduling.guardians_talk_schedule_trimming import apply_guardians_talk_trimming
from .set_itinerary_context import build_set_itinerary_current_itinerary
from .set_itinerary_context import SetItineraryContext
from ...shared.enums import ItineraryErrorType


def commit_set_itinerary(
      context: SetItineraryContext,
      *,
      overriding_conflicting_guardians_talks: bool ) -> ItinerarySaveResult:
   validated_itinerary = context.validated_itinerary

   if overriding_conflicting_guardians_talks:
      trimmed_guardians_talks = apply_guardians_talk_trimming(
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

   clear_itinerary( context.conn )
   save_validated_itinerary(
      context.conn,
      context.save_input.date,
      validated_itinerary )

   return ItinerarySaveResult(
      adjustments=context.adjustments,
      suppressed_warnings=context.suppressed_warnings,
      itinerary=build_set_itinerary_current_itinerary(
         context.conn,
         context.itinerary_controller_kwargs ) )
