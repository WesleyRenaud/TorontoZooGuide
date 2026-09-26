from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_attraction_save_carryover_mapper import ItineraryAttractionSaveCarryoverMapper
from api.shared.date_values import DateValues
from api.shared.enums.position import Position


def Test_MapFromSavedAttractionRows_TestMatchingName_ExpectScheduleCarryover() -> None:
   attraction = 'Conservation Carousel'
   new_likelihood = 100
   start_time = '11:00 AM'
   duration_minutes = 8
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   saved_rows = [
      ItineraryAttractionRecord(
         attraction=attraction,
         old_likelihood=None,
         new_likelihood=new_likelihood,
         start_time=start_time,
         end_time=end_time ),
   ]
   old_visit_date = '2026-06-15'

   carryover = ItineraryAttractionSaveCarryoverMapper.map_from_saved_attraction_rows(
      saved_rows,
      attraction,
      old_visit_date=old_visit_date )

   saved_row = saved_rows[ Position.FIRST ]
   assert carryover.start_time == saved_row.start_time
   assert carryover.end_time == saved_row.end_time
   assert carryover.old_likelihood == saved_row.new_likelihood


def Test_MapFromSavedAttractionRows_TestNoOldVisitDate_ExpectEmptyCarryover() -> None:
   attraction = 'Conservation Carousel'
   start_time = '11:00 AM'
   duration_minutes = 8
   saved_rows = [
      ItineraryAttractionRecord(
         attraction=attraction,
         old_likelihood=None,
         new_likelihood=100,
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) ),
   ]
   old_visit_date = None

   carryover = ItineraryAttractionSaveCarryoverMapper.map_from_saved_attraction_rows(
      saved_rows,
      attraction,
      old_visit_date=old_visit_date )

   assert carryover.start_time is None
   assert carryover.end_time is None
