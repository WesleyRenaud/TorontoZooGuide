from __future__ import annotations

from api.itinerary.data_access.itinerary_event_default_mapper import ItineraryEventDefaultMapper
from api.itinerary.data_access.itinerary_event_default_record import ItineraryEventDefaultRecord
from api.shared.enums import ItineraryEventType, Position


def Test_MapRecord_TestRow_ExpectEventDefaultRecord() -> None:
   event_type = ItineraryEventType.LUNCH
   default_duration_minutes = 40
   row = {
      'EVENT_TYPE': event_type.value,
      'DEFAULT_ITINERARY_DURATION_MINUTES': default_duration_minutes,
   }

   record = ItineraryEventDefaultMapper.map_record( row )

   assert record == ItineraryEventDefaultRecord(
      event_type=ItineraryEventType.normalize( event_type.value ),
      default_duration_minutes=int( default_duration_minutes ) )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   event_type = ItineraryEventType.LUNCH
   default_duration_minutes = 40
   row = {
      'EVENT_TYPE': event_type.value,
      'DEFAULT_ITINERARY_DURATION_MINUTES': default_duration_minutes,
   }
   rows = [ row ]

   records = ItineraryEventDefaultMapper.map_records( rows )

   assert records[ Position.FIRST ].event_type == ItineraryEventType.normalize(
      event_type.value )
