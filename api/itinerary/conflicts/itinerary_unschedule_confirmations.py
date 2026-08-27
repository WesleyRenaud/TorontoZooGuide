from __future__ import annotations

from dataclasses import dataclass

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.unscheduling.fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from ..scheduling.unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from ..scheduling.unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer
from ..warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from ..warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder


@dataclass( frozen=True )
class ItineraryUnscheduleRequirements:
   talks: list[ GuardiansTalkDiff ]
   encounters: list[ WildEncounterDiff ]


def find_itinerary_unschedule_requirements(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary ) -> ItineraryUnscheduleRequirements:
   return ItineraryUnscheduleRequirements(
      talks=GuardiansTalkUnscheduleWarningBuilder.new_talks_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ),
      encounters=WildEncounterUnscheduleWarningBuilder.new_encounters_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ),
   )


def unschedule_confirmation_warning(
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


def apply_confirmed_itinerary_unschedule_changes(
      validated_itinerary: ValidatedItinerary,
      requirements: ItineraryUnscheduleRequirements ) -> ValidatedItinerary:
   activity_blocks = [
      *GuardiansTalkUnschedulePreparer.time_blocks( requirements.talks ),
      *WildEncounterUnschedulePreparer.time_blocks( requirements.encounters ),
   ]

   if not activity_blocks:
      return validated_itinerary

   return FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
      validated_itinerary,
      activity_blocks )
