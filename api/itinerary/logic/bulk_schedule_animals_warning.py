from __future__ import annotations

from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItinerarySaveIssueItemType
from ...shared.enums import ItinerarySaveIssueType


def build_bulk_schedule_animals_not_enough_time_issue(
      animals: list[ ItineraryAnimalRecord ],
) -> ItinerarySaveIssue:
   issue_items = tuple(
      ItinerarySaveIssueItem(
         name=animal.species,
         start_time=None,
         end_time=None,
         item_type=ItinerarySaveIssueItemType.ANIMAL,
         location=animal.exhibit,
      )
      for animal in animals )

   return ItinerarySaveIssue(
      issue_type=ItinerarySaveIssueType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME,
      items=issue_items )
