from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.unscheduling.guardians_talk_unschedule_items import newly_added_active_guardians_talks
from ..scheduling.unscheduling.guardians_talk_unschedule_items import saved_itinerary_has_overlap_with_guardians_talks
from ...shared.enums import ItineraryErrorType


def guardians_talk_unschedule_warning_is_required(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary,
      *,
      confirming_guardians_talk_unschedule: bool ) -> bool:
   if confirming_guardians_talk_unschedule:
      return False

   new_guardians_talks = newly_added_active_guardians_talks(
      saved_itinerary,
      validated_itinerary.guardians_talks )

   if not new_guardians_talks:
      return False

   return saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary,
      new_guardians_talks )


def new_guardians_talks_overlapping_saved_schedule(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary ) -> list[ GuardiansTalkDiff ]:
   new_guardians_talks = newly_added_active_guardians_talks(
      saved_itinerary,
      validated_itinerary.guardians_talks )

   if not new_guardians_talks:
      return []

   if not saved_itinerary_has_overlap_with_guardians_talks(
         saved_itinerary,
         new_guardians_talks ):
      return []

   return new_guardians_talks


def build_guardians_talk_unschedule_issue(
      guardians_talks: list[ GuardiansTalkDiff ] ) -> ItineraryResultReason:
   issue_items = [
      ItinerarySaveIssueItem.from_guardians_talk_diff( guardians_talk )
      for guardians_talk in guardians_talks
   ]

   return ItineraryResultReason(
      code=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      items=issue_items )
