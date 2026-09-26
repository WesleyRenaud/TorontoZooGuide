from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_leg_mapper import ItineraryTransportationLegMapper
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.shared.value_conversion import ValueConversion


def Test_MapRecord_TestRow_ExpectLegWithBoolean() -> None:
   from_station = 'Main Zoomobile Station'
   to_station = 'Africa Zoomobile Station'
   start_time = '11:00 AM'
   duration_minutes = 20
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = 1
   row = {
      'FROM_STATION': from_station,
      'TO_STATION': to_station,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'TRANSPORTATION': transportation,
      'ADDED_AS_ATTRACTION': added_as_attraction,
   }

   leg = ItineraryTransportationLegMapper.map_record( row )

   assert leg.from_station == from_station
   assert leg.to_station == to_station
   assert leg.start_time == start_time
   assert leg.end_time == end_time
   assert leg.transportation == transportation
   assert leg.added_as_attraction is ValueConversion.as_boolean( added_as_attraction )


def Test_MapRecords_TestRows_ExpectLegs() -> None:
   from_station = 'Main Zoomobile Station'
   to_station = 'Africa Zoomobile Station'
   start_time = '11:00 AM'
   duration_minutes = 20
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = 0
   row = {
      'FROM_STATION': from_station,
      'TO_STATION': to_station,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'TRANSPORTATION': transportation,
      'ADDED_AS_ATTRACTION': added_as_attraction,
   }
   rows = [ row ]

   legs = ItineraryTransportationLegMapper.map_records( rows )

   assert len( legs ) == len( rows )
   assert legs[ Position.FIRST ].added_as_attraction is ValueConversion.as_boolean(
      added_as_attraction )
