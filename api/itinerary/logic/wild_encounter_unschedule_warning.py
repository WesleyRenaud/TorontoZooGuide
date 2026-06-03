from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.enums import ItinerarySaveIssueType
from .wild_encounter_unschedule_items import newly_added_active_wild_encounters
from .wild_encounter_unschedule_items import saved_itinerary_has_overlap_with_wild_encounters


def wild_encounters_requiring_unschedule(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary,
) -> list[ WildEncounterDiff ]:
   new_wild_encounters = newly_added_active_wild_encounters(
      saved_itinerary,
      validated_itinerary.wild_encounters )

   if not new_wild_encounters:
      return []

   if not saved_itinerary_has_overlap_with_wild_encounters(
         saved_itinerary,
         new_wild_encounters ):
      return []

   return new_wild_encounters


def build_wild_encounter_unschedule_issue(
      wild_encounters: list[ WildEncounterDiff ],
) -> ItinerarySaveIssue:
   issue_items = tuple(
      ItinerarySaveIssueItem.from_wild_encounter_diff( wild_encounter )
      for wild_encounter in wild_encounters )

   return ItinerarySaveIssue(
      issue_type=ItinerarySaveIssueType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      items=issue_items )
