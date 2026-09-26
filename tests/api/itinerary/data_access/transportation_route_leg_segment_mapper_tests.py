from __future__ import annotations

from api.itinerary.data_access.transportation_route_leg_segment_mapper import TransportationRouteLegSegmentMapper
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.enums.position import Position


def Test_MapRecord_TestRow_ExpectSegment() -> None:
   from_station = 'Main Zoomobile Station'
   to_station = 'Africa Zoomobile Station'
   duration_minutes = '20'
   row = {
      'FROM_STATION': from_station,
      'TO_STATION': to_station,
      'DURATION_MINUTES': duration_minutes,
   }

   segment = TransportationRouteLegSegmentMapper.map_record( row )

   assert segment == TransportationRouteLegSegment(
      from_station=from_station,
      to_station=to_station,
      duration_minutes=int( duration_minutes ) )


def Test_MapRecords_TestRows_ExpectSegments() -> None:
   first_from_station = 'Main Zoomobile Station'
   first_to_station = 'Africa Zoomobile Station'
   first_duration_minutes = 20
   second_from_station = first_to_station
   second_to_station = 'Eurasia Zoomobile Station'
   second_duration_minutes = 15
   first_row = {
      'FROM_STATION': first_from_station,
      'TO_STATION': first_to_station,
      'DURATION_MINUTES': first_duration_minutes,
   }
   second_row = {
      'FROM_STATION': second_from_station,
      'TO_STATION': second_to_station,
      'DURATION_MINUTES': second_duration_minutes,
   }
   rows = [ first_row, second_row ]

   segments = TransportationRouteLegSegmentMapper.map_records( rows )

   assert segments[ Position.FIRST ] == TransportationRouteLegSegment(
      from_station=first_from_station,
      to_station=first_to_station,
      duration_minutes=int( first_duration_minutes ) )
   assert segments[ Position.SECOND ] == TransportationRouteLegSegment(
      from_station=second_from_station,
      to_station=second_to_station,
      duration_minutes=int( second_duration_minutes ) )
