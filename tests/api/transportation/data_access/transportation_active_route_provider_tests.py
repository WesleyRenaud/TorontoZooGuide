from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.transportation.data_access.transportation_active_route_provider import TransportationActiveRouteProvider


TRANSPORTATION_ACTIVE_ROUTE_PROVIDER_SCHEMA = """
CREATE TABLE TransportationRoute (
   TRANSPORTATION   TEXT NOT NULL,
   ROUTE            TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ROUTE )
);

CREATE TABLE TransportationRouteStation (
   TRANSPORTATION   TEXT NOT NULL,
   ROUTE            TEXT NOT NULL,
   STATION          TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ROUTE, STATION )
);

CREATE TABLE TransportationRouteSchedule (
   TRANSPORTATION        TEXT NOT NULL,
   SCHEDULE_START_DATE   TEXT NOT NULL,
   SCHEDULE_END_DATE     TEXT,
   ROUTE                 TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, SCHEDULE_START_DATE )
);

CREATE TABLE TransportationDayRoute (
   TRANSPORTATION   TEXT    NOT NULL,
   MONTH            INTEGER NOT NULL,
   DAY              INTEGER NOT NULL,
   ROUTE            TEXT    NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, MONTH, DAY )
);
"""

ZOOMOBILE = 'Zoomobile'
TRAIN = 'Zoo Train'
SUMMER = 'summer'
WINTER = 'winter'
MAIN = 'Main Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TARGET_DATE = date( 2026, 6, 15 )


@pytest.fixture
def transportation_active_route_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_ACTIVE_ROUTE_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchTransportationRouteIds_TestEmpty_ExpectEmptyList(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationActiveRouteProvider.fetch_transportation_route_ids(
      transportation_active_route_provider_conn,
      ZOOMOBILE ) == []


def Test_FetchTransportationRouteIds_TestPopulated_ExpectFilteredRoutes(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_active_route_provider_conn.executemany(
      """   INSERT INTO TransportationRoute ( TRANSPORTATION, ROUTE )
            VALUES ( ?, ? );
      """,
      [
         ( ZOOMOBILE, SUMMER ),
         ( ZOOMOBILE, WINTER ),
         ( TRAIN, 'loop' ),
      ],
   )
   transportation_active_route_provider_conn.commit()

   routes = TransportationActiveRouteProvider.fetch_transportation_route_ids(
      transportation_active_route_provider_conn,
      ZOOMOBILE )

   assert set( routes ) == { SUMMER, WINTER }


def Test_FetchTransportationRouteStationNames_TestEmpty_ExpectEmptyList(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationActiveRouteProvider.fetch_transportation_route_station_names(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      SUMMER ) == []


def Test_FetchTransportationRouteStationNames_TestPopulated_ExpectFilteredStations(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_active_route_provider_conn.executemany(
      """   INSERT INTO TransportationRouteStation (
               TRANSPORTATION, ROUTE, STATION
            )
            VALUES ( ?, ?, ? );
      """,
      [
         ( ZOOMOBILE, SUMMER, MAIN ),
         ( ZOOMOBILE, SUMMER, AFRICA ),
         ( ZOOMOBILE, WINTER, MAIN ),
      ],
   )
   transportation_active_route_provider_conn.commit()

   stations = TransportationActiveRouteProvider.fetch_transportation_route_station_names(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      SUMMER )

   assert set( stations ) == { MAIN, AFRICA }


def Test_FetchActiveTransportationRoute_TestMissing_ExpectNone(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationActiveRouteProvider.fetch_active_transportation_route(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      TARGET_DATE ) is None


def Test_FetchActiveTransportationRoute_TestExpiredOnly_ExpectNone(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_active_route_provider_conn.execute(
      """   INSERT INTO TransportationRouteSchedule (
               TRANSPORTATION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ROUTE
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, '2026-01-01', '2026-03-31', WINTER ),
   )
   transportation_active_route_provider_conn.commit()

   assert TransportationActiveRouteProvider.fetch_active_transportation_route(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      TARGET_DATE ) is None


def Test_FetchActiveTransportationRoute_TestOpenEndedAndNewerStart_ExpectNewestRoute(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_active_route_provider_conn.executemany(
      """   INSERT INTO TransportationRouteSchedule (
               TRANSPORTATION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ROUTE
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( ZOOMOBILE, '2026-01-01', None, WINTER ),
         ( ZOOMOBILE, '2026-06-01', '2026-08-31', SUMMER ),
      ],
   )
   transportation_active_route_provider_conn.commit()

   route = TransportationActiveRouteProvider.fetch_active_transportation_route(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      TARGET_DATE )

   assert route == SUMMER


def Test_FetchTransportationDayRoute_TestMissing_ExpectNone(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationActiveRouteProvider.fetch_transportation_day_route(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      TARGET_DATE.month,
      TARGET_DATE.day ) is None


def Test_FetchTransportationDayRoute_TestPresent_ExpectRoute(
      transportation_active_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_active_route_provider_conn.execute(
      """   INSERT INTO TransportationDayRoute (
               TRANSPORTATION, MONTH, DAY, ROUTE
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, TARGET_DATE.month, TARGET_DATE.day, SUMMER ),
   )
   transportation_active_route_provider_conn.commit()

   route = TransportationActiveRouteProvider.fetch_transportation_day_route(
      transportation_active_route_provider_conn,
      ZOOMOBILE,
      TARGET_DATE.month,
      TARGET_DATE.day )

   assert route == SUMMER
