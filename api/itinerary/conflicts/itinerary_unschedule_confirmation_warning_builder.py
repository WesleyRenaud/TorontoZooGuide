from __future__ import annotations

from .itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from ...models import Itinerary
from ..results.itinerary_save_result import ItinerarySaveResult
from ..warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from ..warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder


class ItineraryUnscheduleConfirmationWarningBuilder():
   @classmethod
   def build(
         cls,
         requirements: ItineraryUnscheduleRequirements,
         itinerary: Itinerary,
         *,
         confirming_guardians_talk_unschedule: bool,
         confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult | None:
      pending_reasons = []

      if (
            requirements.talks
            and not confirming_guardians_talk_unschedule ):
         pending_reasons.append(
            GuardiansTalkUnscheduleWarningBuilder.build_issue(
               requirements.talks ) )

      if (
            requirements.encounters
            and not confirming_wild_encounter_unschedule ):
         pending_reasons.append(
            WildEncounterUnscheduleWarningBuilder.build_issue(
               requirements.encounters ) )

      if not pending_reasons:
         return None

      return ItinerarySaveResult(
         status=pending_reasons[ 0 ].code,
         reasons=pending_reasons,
         itinerary=itinerary )
