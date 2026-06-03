from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from .guardians_talk_unschedule_items import newly_added_active_guardians_talks
from .guardians_talk_unschedule_items import saved_itinerary_has_overlap_with_guardians_talks
from ...models.guardians_talk_diff import GuardiansTalkDiff


def guardians_talk_unschedule_warning_is_required(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary,
      *,
      confirming_guardians_talk_unschedule: bool,
) -> bool:
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


def guardians_talks_requiring_unschedule(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary,
) -> list[ GuardiansTalkDiff ]:
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
