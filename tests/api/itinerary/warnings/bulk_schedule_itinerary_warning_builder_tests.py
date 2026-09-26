from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.warnings.bulk_schedule_itinerary_warning_builder import BulkScheduleItineraryWarningBuilder
from api.shared.enums import ItineraryErrorType, Position
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums.transportation_name import TransportationName


CAROUSEL = 'Conservation Carousel'


def Test_BuildNotEnoughTimeIssue_TestAnimalAndAttraction_ExpectIssueItems() -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   attraction = ItineraryAttractionRecord(
      attraction=CAROUSEL,
      old_likelihood=None,
      new_likelihood=100 )
   items = [ lion, attraction ]

   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue( items )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert [
      ( item.name, item.item_type, item.location )
      for item in issue.items
   ] == [
      ( lion.species, ItinerarySaveIssueItemType.ANIMAL, lion.exhibit ),
      ( attraction.attraction, ItinerarySaveIssueItemType.ATTRACTION, '' ),
   ]


def Test_BuildNotEnoughTimeIssue_TestPenguinAndLion_ExpectIssueOrderPreserved() -> None:
   penguin = ItineraryAnimalRecord(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   items = [ penguin, lion ]

   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue( items )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert [ item.name for item in issue.items ] == [
      penguin.species,
      lion.species,
   ]
   assert [ item.location for item in issue.items ] == [
      penguin.exhibit,
      lion.exhibit,
   ]


def Test_BuildNotEnoughTimeIssue_TestTransportation_ExpectAttractionIssueItem() -> None:
   transportation = ItineraryTransportationRecord(
      transportation=TransportationName.ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True )

   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue(
      [ transportation ] )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert len( issue.items ) == 1
   assert issue.items[ Position.FIRST ].name == transportation.transportation
   assert issue.items[ Position.FIRST ].item_type == ItinerarySaveIssueItemType.ATTRACTION
