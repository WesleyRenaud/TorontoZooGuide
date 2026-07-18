from __future__ import annotations

from dataclasses import dataclass

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.unscheduling.fixed_time_activity_unschedule_items import prepare_validated_itinerary_for_fixed_time_activity_reschedule
from ..scheduling.unscheduling.guardians_talk_unschedule_items import guardians_talk_time_blocks
from ..scheduling.unscheduling.wild_encounter_unschedule_items import wild_encounter_time_blocks
from ..warnings.guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue
from ..warnings.guardians_talk_unschedule_warning import new_guardians_talks_overlapping_saved_schedule
from ..warnings.wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from ..warnings.wild_encounter_unschedule_warning import new_wild_encounters_overlapping_saved_schedule


@dataclass( frozen=True )
class ItineraryUnscheduleRequirements:
   talks: list[ GuardiansTalkDiff ]
   encounters: list[ WildEncounterDiff ]


def find_itinerary_unschedule_requirements(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary ) -> ItineraryUnscheduleRequirements:
   return ItineraryUnscheduleRequirements(
      talks=new_guardians_talks_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ),
      encounters=new_wild_encounters_overlapping_saved_schedule(
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
         build_guardians_talk_unschedule_issue(
            requirements.talks ) )

   if (
         requirements.encounters
         and not confirming_wild_encounter_unschedule ):
      pending_reasons.append(
         build_wild_encounter_unschedule_issue(
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
      *guardians_talk_time_blocks( requirements.talks ),
      *wild_encounter_time_blocks( requirements.encounters ),
   ]

   if not activity_blocks:
      return validated_itinerary

   return prepare_validated_itinerary_for_fixed_time_activity_reschedule(
      validated_itinerary,
      activity_blocks )
