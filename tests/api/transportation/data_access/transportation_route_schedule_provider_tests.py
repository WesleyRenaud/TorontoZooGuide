from __future__ import annotations

import sqlite3

import pytest

from api.transportation.data_access.transportation_route_schedule_provider import TransportationRouteScheduleProvider
from api.transportation.scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule

TRANSPORTATION_ROUTE_SCHEDULE_PROVIDER_SCHEMA = """
CREATE TABLE Transportation (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   IS_ALSO_ATTRACTION   INTEGER NOT NULL
);

CREATE TABLE TransportationRoute (
   TRANSPORTATION   TEXT NOT NULL,
   ROUTE            TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ROUTE )
);

CREATE TABLE TransportationRouteSchedule (
   TRANSPORTATION        TEXT NOT NULL,
   SCHEDULE_START_DATE   TEXT NOT NULL,
   SCHEDULE_END_DATE     TEXT,
   ROUTE                 TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, SCHEDULE_START_DATE )
);
"""

ZOOMOBILE = 'Zoomobile'

@pytest.fixture
def transportation_route_schedule_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_ROUTE_SCHEDULE_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO Transportation (
               NAME,
               IS_ALSO_ATTRACTION
            )
            VALUES ( ?, 1 );
      """,
      ( ZOOMOBILE, ),
   )
   conn.execute(
      """   INSERT INTO TransportationRoute (
               TRANSPORTATION,
               ROUTE
            )
            VALUES ( ?, ? );
      """,
      ( ZOOMOBILE, 'summer' ),
   )
   conn.commit()

   yield conn

   conn.close()

def Test_SaveCurrentTransportationRouteSchedule_TestInsert_ExpectPersisted(
      transportation_route_schedule_provider_conn: sqlite3.Connection ) -> None:
   schedule = TransportationCurrentRouteSchedule(
      route='summer',
      start_date='2026-05-01',
      end_date='2026-09-30' )

   saved = TransportationRouteScheduleProvider.save_current_transportation_route_schedule(
      transportation_route_schedule_provider_conn,
      ZOOMOBILE,
      schedule )

   row = transportation_route_schedule_provider_conn.execute(
      """   SELECT ROUTE, SCHEDULE_START_DATE, SCHEDULE_END_DATE
            FROM TransportationRouteSchedule
            WHERE TRANSPORTATION = ?;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert saved is True
   assert row is not None
   assert row[ 'ROUTE' ] == 'summer'
   assert row[ 'SCHEDULE_START_DATE' ] == '2026-05-01'
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-09-30'

def Test_SaveCurrentTransportationRouteSchedule_TestReplace_ExpectUpdatedRoute(
      transportation_route_schedule_provider_conn: sqlite3.Connection ) -> None:
   transportation_route_schedule_provider_conn.execute(
      """   INSERT INTO TransportationRoute (
               TRANSPORTATION,
               ROUTE
            )
            VALUES ( ?, ? );
      """,
      ( ZOOMOBILE, 'winter' ),
   )
   transportation_route_schedule_provider_conn.commit()

   TransportationRouteScheduleProvider.save_current_transportation_route_schedule(
      transportation_route_schedule_provider_conn,
      ZOOMOBILE,
      TransportationCurrentRouteSchedule(
         route='summer',
         start_date='2026-05-01',
         end_date=None ) )
   saved = TransportationRouteScheduleProvider.save_current_transportation_route_schedule(
      transportation_route_schedule_provider_conn,
      ZOOMOBILE,
      TransportationCurrentRouteSchedule(
         route='winter',
         start_date='2026-05-01',
         end_date='2026-12-31' ) )

   row = transportation_route_schedule_provider_conn.execute(
      """   SELECT ROUTE, SCHEDULE_END_DATE
            FROM TransportationRouteSchedule
            WHERE TRANSPORTATION = ?
              AND SCHEDULE_START_DATE = ?;
      """,
      ( ZOOMOBILE, '2026-05-01' ),
   ).fetchone()

   assert saved is True
   assert row is not None
   assert row[ 'ROUTE' ] == 'winter'
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-12-31'
