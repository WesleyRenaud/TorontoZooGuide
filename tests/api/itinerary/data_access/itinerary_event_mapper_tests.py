from __future__ import annotations

from api.itinerary.data_access.itinerary_event_mapper import ItineraryEventMapper
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.shared.enums import ItineraryEventType


EVENT_ROW = {
   'EVENT_TYPE': 'lunch',
   'START_TIME': '12:00 PM',
   'END_TIME': '12:30 PM',
}


def Test_MapRecord_TestRow_ExpectEventRecord() -> None:
   assert ItineraryEventMapper.map_record( EVENT_ROW ) == ItineraryEventRecord(
      event_type=ItineraryEventType.LUNCH,
      start_time='12:00 PM',
      end_time='12:30 PM',
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryEventMapper.map_records( [ EVENT_ROW ] )

   assert records[ 0 ].event_type == ItineraryEventType.LUNCH
