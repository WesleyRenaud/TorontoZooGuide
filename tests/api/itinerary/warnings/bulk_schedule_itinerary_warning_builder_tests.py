from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.warnings.bulk_schedule_itinerary_warning_builder import BulkScheduleItineraryWarningBuilder
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType


CAROUSEL = 'Conservation Carousel'


def Test_BuildNotEnoughTimeIssue_TestAnimalAndAttraction_ExpectIssueItems() -> None:
   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert [
      ( item.name, item.item_type, item.location )
      for item in issue.items
   ] == [
      ( 'African Lion', ItinerarySaveIssueItemType.ANIMAL, 'Africa Savanna' ),
      ( CAROUSEL, ItinerarySaveIssueItemType.ATTRACTION, '' ),
   ]


def Test_BuildNotEnoughTimeIssue_TestPenguinAndLion_ExpectIssueOrderPreserved() -> None:
   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue(
      [
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert [ item.name for item in issue.items ] == [
      'African Penguin',
      'African Lion',
   ]
   assert [ item.location for item in issue.items ] == [
      'Africa Savanna',
      'Africa Savanna',
   ]
