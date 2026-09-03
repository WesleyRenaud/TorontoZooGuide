from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider


VISIT_DATE = date( 2026, 6, 15 )
ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

DAY_LOOP_PROVIDER_SCHEMA = """
CREATE TABLE TransportationRouteSchedule (
   TRANSPORTATION           TEXT        NOT NULL,
   ROUTE                    TEXT        NOT NULL,
   SCHEDULE_START_DATE      TEXT        NOT NULL,
   SCHEDULE_END_DATE        TEXT
);

CREATE TABLE TransportationDayRoute (
   TRANSPORTATION           TEXT        NOT NULL,
   ROUTE                    TEXT        NOT NULL,
   MONTH                    INTEGER     NOT NULL,
   DAY                      INTEGER     NOT NULL
);

CREATE TABLE TransportationStation (
   TRANSPORTATION           TEXT        NOT NULL,
   NAME                     TEXT        NOT NULL,
   IS_MAIN_STATION          INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE TransportationRouteLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ROUTE                    TEXT        NOT NULL,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL
);

CREATE TABLE TransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   DURATION_MINUTES         INTEGER     NOT NULL
);
"""


@pytest.fixture
def day_loop_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DAY_LOOP_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO TransportationRouteSchedule (
               TRANSPORTATION,
               ROUTE,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE
            )
            VALUES ( ?, 'winter', '2026-01-01', '2026-03-31' );
      """,
      ( ZOOMOBILE, ) )
   conn.execute(
      """   INSERT INTO TransportationDayRoute (
               TRANSPORTATION,
               ROUTE,
               MONTH,
               DAY
            )
            VALUES ( ?, 'summer', 6, 15 );
      """,
      ( ZOOMOBILE, ) )
   conn.execute(
      """   INSERT INTO TransportationStation (
               TRANSPORTATION,
               NAME,
               IS_MAIN_STATION
            )
            VALUES ( ?, ?, 1 );
      """,
      ( ZOOMOBILE, MAIN ) )
   conn.executemany(
      """   INSERT INTO TransportationRouteLeg (
               TRANSPORTATION,
               ROUTE,
               FROM_STATION,
               TO_STATION
            )
            VALUES ( ?, 'summer', ?, ? );
      """,
      [
         ( ZOOMOBILE, MAIN, CANADA ),
         ( ZOOMOBILE, CANADA, AFRICA ),
      ] )
   conn.executemany(
      """   INSERT INTO TransportationLeg (
               TRANSPORTATION,
               FROM_STATION,
               TO_STATION,
               DURATION_MINUTES
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( ZOOMOBILE, MAIN, CANADA, 20 ),
         ( ZOOMOBILE, CANADA, AFRICA, 10 ),
      ] )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchTransportationActiveRoute_TestVisitDateInRange_ExpectWinterRoute(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_transportation_active_route(
      day_loop_provider_conn,
      transportation=ZOOMOBILE,
      target_date=date( 2026, 2, 1 ) ) == 'winter'


def Test_FetchTransportationDayRoute_TestOwnedDate_ExpectSummerRoute(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_transportation_day_route(
      day_loop_provider_conn,
      transportation=ZOOMOBILE,
      month=6,
      day=15 ) == 'summer'


def Test_FetchMainTransportationStation_TestZoomobile_ExpectMainStation(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_main_transportation_station(
      day_loop_provider_conn,
      ZOOMOBILE ) == MAIN


def Test_FetchTransportationRouteLegs_TestSummerRoute_ExpectMappedSegments(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   legs = TransportationDayLoopProvider.fetch_transportation_route_legs(
      day_loop_provider_conn,
      transportation=ZOOMOBILE,
      route='summer' )

   assert len( legs ) == 2
   assert legs[ 0 ].from_station == MAIN
   assert legs[ 0 ].to_station == CANADA
   assert legs[ 0 ].duration_minutes == 20
   assert legs[ 1 ].from_station == CANADA
   assert legs[ 1 ].to_station == AFRICA
   assert legs[ 1 ].duration_minutes == 10


def Test_FetchTransportationActiveRoute_TestMissingSchedule_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_transportation_active_route(
      day_loop_provider_conn,
      transportation=ZOOMOBILE,
      target_date=date( 2026, 7, 1 ) ) is None


def Test_FetchTransportationDayRoute_TestMissingDate_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_transportation_day_route(
      day_loop_provider_conn,
      transportation=ZOOMOBILE,
      month=7,
      day=4 ) is None


def Test_FetchMainTransportationStation_TestMissingStation_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationDayLoopProvider.fetch_main_transportation_station(
      day_loop_provider_conn,
      'Tundra Trek Ride' ) is None
