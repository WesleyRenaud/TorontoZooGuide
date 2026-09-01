from __future__ import annotations

from api.itinerary.data_access.itinerary_event_default_mapper import ItineraryEventDefaultMapper
from api.itinerary.data_access.itinerary_event_default_record import ItineraryEventDefaultRecord
from api.shared.enums import ItineraryEventType


LUNCH_ROW = {
   'EVENT_TYPE': 'lunch',
   'DEFAULT_ITINERARY_DURATION_MINUTES': 40,
}


def Test_MapRecord_TestRow_ExpectEventDefaultRecord() -> None:
   assert ItineraryEventDefaultMapper.map_record( LUNCH_ROW ) == ItineraryEventDefaultRecord(
      event_type=ItineraryEventType.LUNCH,
      default_duration_minutes=40,
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryEventDefaultMapper.map_records( [ LUNCH_ROW ] )

   assert records[ 0 ].event_type == ItineraryEventType.LUNCH
