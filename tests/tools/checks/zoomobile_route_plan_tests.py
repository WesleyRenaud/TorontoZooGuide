from __future__ import annotations

from datetime import date

from api.shared.enums.transportation_route_id import TransportationRouteId
from api.transportation.scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from tools.checks.zoomobile_route_builder import ZoomobileRouteBuilder


SUMMER = TransportationRouteId.SUMMER.value
WINTER = TransportationRouteId.WINTER.value


def schedule( route: str, start: str, end: str | None ) -> TransportationCurrentRouteSchedule:
   return TransportationCurrentRouteSchedule( route, start, end )


def Test_Through_TestWebsiteRoute_ExpectScheduledEnd() -> None:
   cases = [
      ( date( 2026, 5, 1 ), SUMMER, date( 2026, 10, 31 ) ),
      ( date( 2026, 5, 1 ), WINTER, date( 2026, 5, 15 ) ),
      ( date( 2026, 7, 1 ), SUMMER, date( 2026, 10, 31 ) ),
      ( date( 2026, 7, 1 ), WINTER, date( 2026, 7, 15 ) ),
      ( date( 2026, 10, 20 ), SUMMER, date( 2026, 10, 31 ) ),
      ( date( 2026, 10, 20 ), WINTER, date( 2027, 4, 30 ) ),
      ( date( 2026, 11, 14 ), WINTER, date( 2027, 4, 30 ) ),
      ( date( 2026, 11, 14 ), SUMMER, date( 2026, 11, 28 ) ),
      ( date( 2027, 1, 5 ), WINTER, date( 2027, 4, 30 ) ),
      ( date( 2027, 1, 5 ), SUMMER, date( 2027, 1, 19 ) ),
      ( date( 2027, 4, 15 ), WINTER, date( 2027, 4, 30 ) ),
      ( date( 2027, 4, 15 ), SUMMER, date( 2027, 10, 31 ) ),
   ]

   assert [
      ZoomobileRouteBuilder.through( route, today )
      for today, route, _end in cases
   ] == [ end for _today, _route, end in cases ]


def Test_Build_TestSameRouteAndEnd_ExpectNoWrite() -> None:
   plan = ZoomobileRouteBuilder.build(
      SUMMER,
      [ schedule( SUMMER, '2026-05-01', '2026-10-31' ) ],
      date( 2026, 7, 1 ),
   )

   assert plan.writes == []


def Test_Build_TestLongerEnd_ExpectTrimmed() -> None:
   plan = ZoomobileRouteBuilder.build(
      SUMMER,
      [ schedule( SUMMER, '2026-11-01', '2026-12-31' ) ],
      date( 2026, 11, 14 ),
   )

   assert [ ( change.route, change.start, change.end ) for change in plan.writes ] == [
      ( SUMMER, date( 2026, 11, 1 ), date( 2026, 11, 28 ) ),
   ]


def Test_Build_TestOlderRowPastTheEnd_ExpectItDoesNotResume() -> None:
   plan = ZoomobileRouteBuilder.build(
      SUMMER,
      [
         schedule( SUMMER, '2026-05-01', '2026-12-31' ),
         schedule( WINTER, '2026-11-08', '2027-04-30' ),
      ],
      date( 2026, 11, 14 ),
   )

   assert [ ( change.route, change.start, change.end ) for change in plan.writes ] == [
      ( SUMMER, date( 2026, 5, 1 ), date( 2026, 11, 13 ) ),
      ( WINTER, date( 2026, 11, 8 ), date( 2026, 11, 13 ) ),
      ( SUMMER, date( 2026, 11, 14 ), date( 2026, 11, 28 ) ),
   ]


def Test_Build_TestOtherRoute_ExpectReplacedFromToday() -> None:
   plan = ZoomobileRouteBuilder.build(
      SUMMER,
      [ schedule( WINTER, '2026-11-08', '2027-04-30' ) ],
      date( 2026, 11, 14 ),
   )

   assert [ ( change.route, change.start, change.end ) for change in plan.writes ] == [
      ( WINTER, date( 2026, 11, 8 ), date( 2026, 11, 13 ) ),
      ( SUMMER, date( 2026, 11, 14 ), date( 2026, 11, 28 ) ),
   ]
