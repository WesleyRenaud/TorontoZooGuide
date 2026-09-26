from __future__ import annotations

import pytest

from api.itinerary.transportation.transportation_route_leg_orderer import TransportationRouteLegOrderer
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.enums.position import Position


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'

SUMMER_LEG_STATIONS = [
   ( MAIN, CANADA ),
   ( CANADA, AFRICA ),
   ( AFRICA, TUNDRA ),
   ( TUNDRA, EURASIA ),
   ( EURASIA, MAIN ),
]


def Test_OrderFromStation_TestUnorderedLegs_ExpectClosedLoop() -> None:
   unordered = [
      TransportationRouteLegSegment(
         from_station=AFRICA,
         to_station=TUNDRA,
         duration_minutes=15 ),
      TransportationRouteLegSegment(
         from_station=MAIN,
         to_station=CANADA,
         duration_minutes=20 ),
      TransportationRouteLegSegment(
         from_station=EURASIA,
         to_station=MAIN,
         duration_minutes=15 ),
      TransportationRouteLegSegment(
         from_station=CANADA,
         to_station=AFRICA,
         duration_minutes=10 ),
      TransportationRouteLegSegment(
         from_station=TUNDRA,
         to_station=EURASIA,
         duration_minutes=15 ),
   ]
   start_station = MAIN

   ordered = TransportationRouteLegOrderer.order_from_station(
      unordered,
      start_station=start_station )

   assert [
      ( leg.from_station, leg.to_station )
      for leg in ordered
   ] == SUMMER_LEG_STATIONS
   assert ordered[ Position.FIRST ].from_station == start_station
   assert sum( leg.duration_minutes for leg in ordered ) == sum(
      leg.duration_minutes for leg in unordered )


def Test_OrderFromStation_TestEmptyLegs_ExpectEmpty() -> None:
   legs: list[ TransportationRouteLegSegment ] = []
   start_station = MAIN

   ordered = TransportationRouteLegOrderer.order_from_station(
      legs,
      start_station=start_station )

   assert ordered == []


def Test_OrderFromStation_TestDuplicateFromStation_ExpectValueError() -> None:
   start_station = MAIN
   legs = [
      TransportationRouteLegSegment(
         from_station=MAIN,
         to_station=CANADA,
         duration_minutes=10 ),
      TransportationRouteLegSegment(
         from_station=MAIN,
         to_station=AFRICA,
         duration_minutes=10 ),
   ]

   with pytest.raises( ValueError, match='Duplicate outgoing leg' ):
      TransportationRouteLegOrderer.order_from_station(
         legs,
         start_station=start_station )


def Test_OrderFromStation_TestMissingOutgoingLeg_ExpectValueError() -> None:
   start_station = MAIN
   legs = [
      TransportationRouteLegSegment(
         from_station=CANADA,
         to_station=AFRICA,
         duration_minutes=10 ),
   ]

   with pytest.raises( ValueError, match='No outgoing leg' ):
      TransportationRouteLegOrderer.order_from_station(
         legs,
         start_station=start_station )


def Test_OrderFromStation_TestOpenLoop_ExpectValueError() -> None:
   start_station = MAIN
   legs = [
      TransportationRouteLegSegment(
         from_station=MAIN,
         to_station=CANADA,
         duration_minutes=10 ),
      TransportationRouteLegSegment(
         from_station=CANADA,
         to_station=AFRICA,
         duration_minutes=10 ),
   ]

   with pytest.raises( ValueError, match='closed loop' ):
      TransportationRouteLegOrderer.order_from_station(
         legs,
         start_station=start_station )
