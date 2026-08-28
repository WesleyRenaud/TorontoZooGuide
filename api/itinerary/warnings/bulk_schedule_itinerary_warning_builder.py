from __future__ import annotations

from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.bulk.loop_schedule_stop import LoopScheduleStop
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType


class BulkScheduleItineraryWarningBuilder():
   @classmethod
   def build_not_enough_time_issue(
         cls,
         stops: list[ LoopScheduleStop.Stop ] ) -> ItineraryResultReason:
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

         if isinstance( stop, ItineraryTransportationRecord ):
            issue_items.append(
               ItinerarySaveIssueItem(
                  name=stop.transportation,
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
         code=ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME,
         items=issue_items )
