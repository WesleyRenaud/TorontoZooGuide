from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_leg_mapper import ItineraryTransportationLegMapper


def Test_MapRecord_TestRow_ExpectLegWithBoolean() -> None:
   leg = ItineraryTransportationLegMapper.map_record(
      {
         'FROM_STATION': 'Main Zoomobile Station',
         'TO_STATION': 'Africa Zoomobile Station',
         'START_TIME': '11:00 AM',
         'END_TIME': '11:20 AM',
         'TRANSPORTATION': 'Zoomobile',
         'ADDED_AS_ATTRACTION': 1,
      } )

   assert leg.from_station == 'Main Zoomobile Station'
   assert leg.to_station == 'Africa Zoomobile Station'
   assert leg.start_time == '11:00 AM'
   assert leg.end_time == '11:20 AM'
   assert leg.transportation == 'Zoomobile'
   assert leg.added_as_attraction is True


def Test_MapRecords_TestRows_ExpectLegs() -> None:
   legs = ItineraryTransportationLegMapper.map_records(
      [
         {
            'FROM_STATION': 'Main Zoomobile Station',
            'TO_STATION': 'Africa Zoomobile Station',
            'START_TIME': '11:00 AM',
            'END_TIME': '11:20 AM',
            'TRANSPORTATION': 'Zoomobile',
            'ADDED_AS_ATTRACTION': 0,
         },
      ] )

   assert len( legs ) == 1
   assert legs[ 0 ].added_as_attraction is False
