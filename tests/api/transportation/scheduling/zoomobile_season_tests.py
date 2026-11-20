from __future__ import annotations

from api.shared.enums.transportation_name import TransportationName
from api.shared.enums.transportation_route_id import TransportationRouteId
from api.transportation.scheduling.zoomobile_season import ZoomobileSeason


SUMMER = TransportationRouteId.SUMMER.value
WINTER = TransportationRouteId.WINTER.value


def Test_RouteFor_TestJune_ExpectSummer() -> None:
   route = ZoomobileSeason.route_for( TransportationName.ZOOMOBILE, 6 )

   assert route == SUMMER


def Test_RouteFor_TestOctober_ExpectSummer() -> None:
   route = ZoomobileSeason.route_for( TransportationName.ZOOMOBILE, 10 )

   assert route == SUMMER


def Test_RouteFor_TestApril_ExpectWinter() -> None:
   route = ZoomobileSeason.route_for( TransportationName.ZOOMOBILE, 4 )

   assert route == WINTER


def Test_RouteFor_TestNovember_ExpectWinter() -> None:
   route = ZoomobileSeason.route_for( TransportationName.ZOOMOBILE, 11 )

   assert route == WINTER


def Test_RouteFor_TestOtherTransportation_ExpectNone() -> None:
   route = ZoomobileSeason.route_for( 'Tundra Trek Ride', 6 )

   assert route is None


def Test_RouteFor_TestMonthOutsideTheWindows_ExpectNone() -> None:
   route = ZoomobileSeason.route_for( TransportationName.ZOOMOBILE, 13 )

   assert route is None
