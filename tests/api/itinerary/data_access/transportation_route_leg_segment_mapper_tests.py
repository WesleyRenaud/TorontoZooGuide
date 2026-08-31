from __future__ import annotations

from api.itinerary.data_access.transportation_route_leg_segment_mapper import TransportationRouteLegSegmentMapper
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


def Test_MapRecord_TestRow_ExpectSegment() -> None:
   segment = TransportationRouteLegSegmentMapper.map_record(
      {
         'FROM_STATION': 'Main Zoomobile Station',
         'TO_STATION': 'Africa Zoomobile Station',
         'DURATION_MINUTES': '20',
      } )

   assert segment == TransportationRouteLegSegment(
      from_station='Main Zoomobile Station',
      to_station='Africa Zoomobile Station',
      duration_minutes=20 )


def Test_MapRecords_TestRows_ExpectSegments() -> None:
   segments = TransportationRouteLegSegmentMapper.map_records(
      [
         {
            'FROM_STATION': 'Main Zoomobile Station',
            'TO_STATION': 'Africa Zoomobile Station',
            'DURATION_MINUTES': 20,
         },
         {
            'FROM_STATION': 'Africa Zoomobile Station',
            'TO_STATION': 'Eurasia Zoomobile Station',
            'DURATION_MINUTES': 15,
         },
      ] )

   assert [
      ( segment.from_station, segment.to_station, segment.duration_minutes )
      for segment in segments
   ] == [
      ( 'Main Zoomobile Station', 'Africa Zoomobile Station', 20 ),
      ( 'Africa Zoomobile Station', 'Eurasia Zoomobile Station', 15 ),
   ]
