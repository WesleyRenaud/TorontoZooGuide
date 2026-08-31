from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_attraction_save_carryover_mapper import ItineraryAttractionSaveCarryoverMapper


CAROUSEL = 'Conservation Carousel'


def Test_MapFromSavedAttractionRows_TestMatchingName_ExpectScheduleCarryover() -> None:
   carryover = ItineraryAttractionSaveCarryoverMapper.map_from_saved_attraction_rows(
      [
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      CAROUSEL,
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time == '11:00 AM'
   assert carryover.end_time == '11:08 AM'
   assert carryover.old_likelihood == 100


def Test_MapFromSavedAttractionRows_TestNoOldVisitDate_ExpectEmptyCarryover() -> None:
   carryover = ItineraryAttractionSaveCarryoverMapper.map_from_saved_attraction_rows(
      [
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      CAROUSEL,
      old_visit_date=None,
   )

   assert carryover.start_time is None
   assert carryover.end_time is None
