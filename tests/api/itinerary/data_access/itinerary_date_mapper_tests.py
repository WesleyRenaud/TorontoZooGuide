from __future__ import annotations

from api.itinerary.data_access.itinerary_date_mapper import ItineraryDateMapper
from api.itinerary.data_access.itinerary_date_record import ItineraryDateRecord
from api.shared.date_values import DateValues


def Test_MapRecord_TestRow_ExpectNormalizedDateRecord() -> None:
   itinerary_date = '2026-06-15'
   arrival_time = '09:30'
   departure_time = '17:00'
   row = {
      'ITINERARY_DATE': itinerary_date,
      'ARRIVAL_TIME': arrival_time,
      'DEPARTURE_TIME': departure_time,
   }

   record = ItineraryDateMapper.map_record( row )

   assert record == ItineraryDateRecord(
      itinerary_date=DateValues.normalize_date_key( itinerary_date ),
      arrival_time=DateValues.normalize_itinerary_schedule_time( arrival_time ),
      departure_time=DateValues.normalize_itinerary_schedule_time( departure_time ) )


def Test_MapRecord_TestMissingRow_ExpectNone() -> None:
   row = None

   record = ItineraryDateMapper.map_record( row )

   assert record is None
