from __future__ import annotations

from api.itinerary.data_access.itinerary_date_mapper import ItineraryDateMapper
from api.itinerary.data_access.itinerary_date_record import ItineraryDateRecord


DATE_ROW = {
   'ITINERARY_DATE': '2026-06-15',
   'ARRIVAL_TIME': '09:30',
   'DEPARTURE_TIME': '17:00',
}


def Test_MapRecord_TestRow_ExpectNormalizedDateRecord() -> None:
   assert ItineraryDateMapper.map_record( DATE_ROW ) == ItineraryDateRecord(
      itinerary_date='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )


def Test_MapRecord_TestMissingRow_ExpectNone() -> None:
   assert ItineraryDateMapper.map_record( None ) is None
