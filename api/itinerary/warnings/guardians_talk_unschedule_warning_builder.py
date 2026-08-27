from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from ...shared.enums import ItineraryErrorType


class GuardiansTalkUnscheduleWarningBuilder():
   @classmethod
   def is_required(
         cls,
         saved_itinerary: SavedItinerary,
         validated_itinerary: ValidatedItinerary,
         *,
         confirming_guardians_talk_unschedule: bool ) -> bool:
      if confirming_guardians_talk_unschedule:
         return False

      new_guardians_talks = GuardiansTalkUnschedulePreparer.newly_added_active(
         saved_itinerary,
         validated_itinerary.guardians_talks )

      if not new_guardians_talks:
         return False

      return GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap(
         saved_itinerary,
         new_guardians_talks )


   @classmethod
   def new_talks_overlapping_saved_schedule(
         cls,
         saved_itinerary: SavedItinerary,
         validated_itinerary: ValidatedItinerary ) -> list[ GuardiansTalkDiff ]:
      new_guardians_talks = GuardiansTalkUnschedulePreparer.newly_added_active(
         saved_itinerary,
         validated_itinerary.guardians_talks )

      if not new_guardians_talks:
         return []

      if not GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap(
            saved_itinerary,
            new_guardians_talks ):
         return []

      return new_guardians_talks


   @classmethod
   def build_issue(
         cls,
         guardians_talks: list[ GuardiansTalkDiff ] ) -> ItineraryResultReason:
      issue_items = [
         ItinerarySaveIssueItem.from_guardians_talk_diff( guardians_talk )
         for guardians_talk in guardians_talks
      ]

      return ItineraryResultReason(
         code=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         items=issue_items )
