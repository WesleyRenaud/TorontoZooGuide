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
from ...shared.enums import ItineraryErrorType
from ..warnings.guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue
from ..warnings.guardians_talk_unschedule_warning import new_guardians_talks_overlapping_saved_schedule
from ..warnings.wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from ..warnings.wild_encounter_unschedule_warning import new_wild_encounters_overlapping_saved_schedule


@dataclass( frozen=True )
class ItineraryUnscheduleRequirements:
   talks: tuple[ GuardiansTalkDiff, ... ]
   encounters: tuple[ WildEncounterDiff, ... ]


def find_itinerary_unschedule_requirements(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary ) -> ItineraryUnscheduleRequirements:
   return ItineraryUnscheduleRequirements(
      talks=tuple(
         new_guardians_talks_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ) ),
      encounters=tuple(
         new_wild_encounters_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ) ),
   )


def unschedule_confirmation_warning(
      requirements: ItineraryUnscheduleRequirements,
      itinerary: Itinerary,
      *,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult | None:
   if (
         requirements.talks
         and not confirming_guardians_talk_unschedule ):
      return ItinerarySaveResult(
         status=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_guardians_talk_unschedule_issue(
               list( requirements.talks ) ),
         ),
         itinerary=itinerary )

   if (
         requirements.encounters
         and not confirming_wild_encounter_unschedule ):
      return ItinerarySaveResult(
         status=ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_wild_encounter_unschedule_issue(
               list( requirements.encounters ) ),
         ),
         itinerary=itinerary )

   return None


def apply_confirmed_itinerary_unschedule_changes(
      validated_itinerary: ValidatedItinerary,
      requirements: ItineraryUnscheduleRequirements ) -> ValidatedItinerary:
   activity_blocks = [
      *guardians_talk_time_blocks( list( requirements.talks ) ),
      *wild_encounter_time_blocks( list( requirements.encounters ) ),
   ]

   if not activity_blocks:
      return validated_itinerary

   return prepare_validated_itinerary_for_fixed_time_activity_reschedule(
      validated_itinerary,
      activity_blocks )
