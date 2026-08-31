from __future__ import annotations

from api.itinerary.transportation.transportation_route_leg_orderer import TransportationRouteLegOrderer
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


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

   ordered = TransportationRouteLegOrderer.order_from_station(
      unordered,
      start_station=MAIN )

   assert [
      ( leg.from_station, leg.to_station )
      for leg in ordered
   ] == SUMMER_LEG_STATIONS
   assert sum( leg.duration_minutes for leg in ordered ) == 75
