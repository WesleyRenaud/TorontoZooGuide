from __future__ import annotations

from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.bulk.loop_schedule_stop import LoopScheduleStop
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType


def build_bulk_schedule_animals_not_enough_time_issue(
      stops: list[ LoopScheduleStop ] ) -> ItineraryResultReason:
   issue_items: list[ ItinerarySaveIssueItem ] = []

   for stop in stops:
      if isinstance( stop, ItineraryAttractionRecord ):
         issue_items.append(
            ItinerarySaveIssueItem(
               name=stop.attraction,
               start_time=None,
               end_time=None,
               item_type=ItinerarySaveIssueItemType.ATTRACTION,
               location='',
            ) )
         continue

      issue_items.append(
         ItinerarySaveIssueItem(
            name=stop.species,
            start_time=None,
            end_time=None,
            item_type=ItinerarySaveIssueItemType.ANIMAL,
            location=stop.exhibit,
         ) )

   return ItineraryResultReason(
      code=ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME,
      items=issue_items )
