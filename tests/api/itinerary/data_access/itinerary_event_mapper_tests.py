from __future__ import annotations

from api.itinerary.data_access.itinerary_event_mapper import ItineraryEventMapper
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.shared.date_values import DateValues
from api.shared.enums import ItineraryEventType, Position


def Test_MapRecord_TestRow_ExpectEventRecord() -> None:
   event_type = ItineraryEventType.LUNCH
   start_time = '12:00 PM'
   duration_minutes = 30
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'EVENT_TYPE': event_type.value,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }

   record = ItineraryEventMapper.map_record( row )

   assert record == ItineraryEventRecord(
      event_type=ItineraryEventType.normalize( event_type.value ),
      start_time=start_time,
      end_time=end_time )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   event_type = ItineraryEventType.LUNCH
   start_time = '12:00 PM'
   duration_minutes = 30
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'EVENT_TYPE': event_type.value,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }
   rows = [ row ]

   records = ItineraryEventMapper.map_records( rows )

   assert records[ Position.FIRST ].event_type == ItineraryEventType.normalize(
      event_type.value )
