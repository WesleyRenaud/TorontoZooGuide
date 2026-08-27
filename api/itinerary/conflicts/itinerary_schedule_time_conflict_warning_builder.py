from __future__ import annotations

from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_save_result import ItinerarySaveResult
from .schedule_time_conflict_issue_finder import ScheduleTimeConflictIssueFinder
from ...shared.enums import ItineraryErrorType


class ItineraryScheduleTimeConflictWarningBuilder():
   @classmethod
   def build(
         cls,
         guardians_talks: list[ GuardiansTalkDiff ],
         wild_encounters: list[ WildEncounterDiff ],
         itinerary: Itinerary,
         *,
         overriding_conflicting_guardians_talks: bool ) -> ItinerarySaveResult | None:
      conflict_issues = ScheduleTimeConflictIssueFinder.find(
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
