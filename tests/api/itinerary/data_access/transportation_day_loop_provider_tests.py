from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


VISIT_DATE = date( 2026, 6, 15 )
WINTER_ROUTE = 'winter'
SUMMER_ROUTE = 'summer'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
MAIN_TO_CANADA_MINUTES = 20
CANADA_TO_AFRICA_MINUTES = 10


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
            VALUES ( ?, ?, '2026-01-01', '2026-03-31' );
      """,
      ( TransportationName.ZOOMOBILE, WINTER_ROUTE ) )
   conn.execute(
      """   INSERT INTO TransportationDayRoute (
               TRANSPORTATION,
               ROUTE,
               MONTH,
               DAY
            )
            VALUES ( ?, ?, ?, ? );
      """,
      (
         TransportationName.ZOOMOBILE,
         SUMMER_ROUTE,
         VISIT_DATE.month,
         VISIT_DATE.day,
      ) )
   conn.execute(
      """   INSERT INTO TransportationStation (
               TRANSPORTATION,
               NAME,
               IS_MAIN_STATION
            )
            VALUES ( ?, ?, 1 );
      """,
      ( TransportationName.ZOOMOBILE, MAIN ) )
   conn.executemany(
      """   INSERT INTO TransportationRouteLeg (
               TRANSPORTATION,
               ROUTE,
               FROM_STATION,
               TO_STATION
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( TransportationName.ZOOMOBILE, SUMMER_ROUTE, MAIN, CANADA ),
         ( TransportationName.ZOOMOBILE, SUMMER_ROUTE, CANADA, AFRICA ),
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
         ( TransportationName.ZOOMOBILE, MAIN, CANADA, MAIN_TO_CANADA_MINUTES ),
         ( TransportationName.ZOOMOBILE, CANADA, AFRICA, CANADA_TO_AFRICA_MINUTES ),
      ] )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchTransportationActiveRoute_TestVisitDateInRange_ExpectWinterRoute(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   target_date = date( 2026, 2, 1 )
   transportation = TransportationName.ZOOMOBILE

   route = TransportationDayLoopProvider.fetch_transportation_active_route(
      day_loop_provider_conn,
      transportation=transportation,
      target_date=target_date )

   assert route == WINTER_ROUTE


def Test_FetchTransportationDayRoute_TestOwnedDate_ExpectSummerRoute(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE

   route = TransportationDayLoopProvider.fetch_transportation_day_route(
      day_loop_provider_conn,
      transportation=transportation,
      month=VISIT_DATE.month,
      day=VISIT_DATE.day )

   assert route == SUMMER_ROUTE


def Test_FetchMainTransportationStation_TestZoomobile_ExpectMainStation(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE

   station = TransportationDayLoopProvider.fetch_main_transportation_station(
      day_loop_provider_conn,
      transportation )

   assert station == MAIN


def Test_FetchTransportationRouteLegs_TestSummerRoute_ExpectMappedSegments(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   route = SUMMER_ROUTE

   legs = TransportationDayLoopProvider.fetch_transportation_route_legs(
      day_loop_provider_conn,
      transportation=transportation,
      route=route )

   assert len( legs ) == 2
   assert legs[ Position.FIRST ].from_station == MAIN
   assert legs[ Position.FIRST ].to_station == CANADA
   assert legs[ Position.FIRST ].duration_minutes == MAIN_TO_CANADA_MINUTES
   assert legs[ Position.SECOND ].from_station == CANADA
   assert legs[ Position.SECOND ].to_station == AFRICA
   assert legs[ Position.SECOND ].duration_minutes == CANADA_TO_AFRICA_MINUTES


def Test_FetchTransportationActiveRoute_TestMissingSchedule_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   target_date = date( 2026, 7, 1 )
   transportation = TransportationName.ZOOMOBILE

   route = TransportationDayLoopProvider.fetch_transportation_active_route(
      day_loop_provider_conn,
      transportation=transportation,
      target_date=target_date )

   assert route is None


def Test_FetchTransportationDayRoute_TestMissingDate_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   month = 7
   day = 4

   route = TransportationDayLoopProvider.fetch_transportation_day_route(
      day_loop_provider_conn,
      transportation=transportation,
      month=month,
      day=day )

   assert route is None


def Test_FetchMainTransportationStation_TestMissingStation_ExpectNone(
      day_loop_provider_conn: sqlite3.Connection ) -> None:
   transportation = 'Tundra Trek Ride'

   station = TransportationDayLoopProvider.fetch_main_transportation_station(
      day_loop_provider_conn,
      transportation )

   assert station is None
