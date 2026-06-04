from __future__ import annotations

from .itinerary_save_result import ItinerarySaveResult
from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.enums import ItineraryErrorType
from .wild_encounter_time_conflicts import find_schedule_time_conflict_issues


def schedule_time_conflict_warning(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ],
      itinerary: Itinerary,
      *,
      overriding_conflicting_guardians_talks: bool ) -> ItinerarySaveResult | None:
   conflict_issues = find_schedule_time_conflict_issues(
      guardians_talks,
      wild_encounters )

   if (
         conflict_issues
         and not overriding_conflicting_guardians_talks ):
      return ItinerarySaveResult(
         status=ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
         reasons=conflict_issues,
         itinerary=itinerary )

   return None
