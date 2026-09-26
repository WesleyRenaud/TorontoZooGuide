from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_mapper import ItineraryAttractionMapper
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.shared.date_values import DateValues
from api.shared.enums.position import Position


def Test_MapRecord_TestRow_ExpectAttractionRecord() -> None:
   attraction = 'Conservation Carousel'
   old_likelihood = None
   new_likelihood = 100
   start_time = '11:00 AM'
   duration_minutes = 20
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'ATTRACTION': attraction,
      'OLD_LIKELIHOOD': old_likelihood,
      'NEW_LIKELIHOOD': new_likelihood,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }

   record = ItineraryAttractionMapper.map_record( row )

   assert record == ItineraryAttractionRecord(
      attraction=attraction,
      old_likelihood=old_likelihood,
      new_likelihood=new_likelihood,
      start_time=start_time,
      end_time=end_time )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   attraction = 'Conservation Carousel'
   old_likelihood = None
   new_likelihood = 100
   start_time = '11:00 AM'
   duration_minutes = 20
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'ATTRACTION': attraction,
      'OLD_LIKELIHOOD': old_likelihood,
      'NEW_LIKELIHOOD': new_likelihood,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }
   rows = [ row ]

   records = ItineraryAttractionMapper.map_records( rows )

   assert records[ Position.FIRST ].attraction == attraction
