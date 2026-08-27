from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer
from ...shared.enums import ItineraryErrorType


class WildEncounterUnscheduleWarningBuilder():
   @classmethod
   def new_encounters_overlapping_saved_schedule(
         cls,
         saved_itinerary: SavedItinerary,
         validated_itinerary: ValidatedItinerary ) -> list[ WildEncounterDiff ]:
      new_wild_encounters = WildEncounterUnschedulePreparer.newly_added_active(
         saved_itinerary,
         validated_itinerary.wild_encounters )

      if not new_wild_encounters:
         return []

      if not WildEncounterUnschedulePreparer.saved_itinerary_has_overlap(
            saved_itinerary,
            new_wild_encounters ):
         return []

      return new_wild_encounters


   @classmethod
   def build_issue(
         cls,
         wild_encounters: list[ WildEncounterDiff ] ) -> ItineraryResultReason:
      issue_items = [
         ItinerarySaveIssueItem.from_wild_encounter_diff( wild_encounter )
         for wild_encounter in wild_encounters
      ]

      return ItineraryResultReason(
         code=ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         items=issue_items )
