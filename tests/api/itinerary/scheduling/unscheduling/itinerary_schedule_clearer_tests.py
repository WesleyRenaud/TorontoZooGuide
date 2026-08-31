from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.scheduling.unscheduling.itinerary_schedule_clearer import ItineraryScheduleClearer
from api.shared.enums import ItineraryEventType


CAROUSEL = 'Conservation Carousel'

SCHEDULE_CLEARER_SCHEMA = """
CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT        NOT NULL,
   EXHIBIT              TEXT        NOT NULL,
   ENCLOSURE_NAME       TEXT,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK      INTEGER     NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   START_TIME               TEXT        NOT NULL,
   END_TIME                 TEXT        NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER     NOT NULL,
   MARKER_ORDER             INTEGER     NOT NULL,
   MARKER_ID                TEXT        NOT NULL
);

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryWalkRouteStop (
   STOP_SEQUENCE          INTEGER     NOT NULL,
   SCHEDULE_ITEM_KIND     TEXT        NOT NULL,
   ITEM_KEY               TEXT        NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   START_TIME             TEXT,
   END_TIME               TEXT,
   PRIMARY KEY ( STOP_SEQUENCE )
);

CREATE TABLE ItineraryWalkRoutePoint (
   POINT_SEQUENCE         INTEGER     NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   X                      REAL        NOT NULL,
   Y                      REAL        NOT NULL,
   X_PX                   REAL        NOT NULL,
   Y_PX                   REAL        NOT NULL,
   PRIMARY KEY ( POINT_SEQUENCE )
);

CREATE TABLE ItineraryWalkRouteLeg (
   LEG_SEQUENCE               INTEGER     NOT NULL,
   FROM_ITEM_KEY              TEXT        NOT NULL,
   TO_ITEM_KEY                TEXT        NOT NULL,
   FROM_SCHEDULE_ITEM_KIND    TEXT        NOT NULL,
   TO_SCHEDULE_ITEM_KIND      TEXT        NOT NULL,
   FROM_POINT_SEQUENCE        INTEGER     NOT NULL,
   TO_POINT_SEQUENCE          INTEGER     NOT NULL,
   TRAVEL_TIME_MINUTES        INTEGER     NOT NULL DEFAULT 0,
   PRIMARY KEY ( LEG_SEQUENCE )
);
"""


@pytest.fixture
def schedule_clearer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEDULE_CLEARER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, ?, ?, 1 );
      """,
      ( 'African Lion', 'Africa Savanna', '10:00 AM', '10:08 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( CAROUSEL, '11:00 AM', '11:20 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:00 PM', '12:30 PM' ) )
   conn.execute(
      """   INSERT INTO ItineraryWalkRouteStop (
               STOP_SEQUENCE,
               SCHEDULE_ITEM_KIND,
               ITEM_KEY,
               WALK_NODE_ID
            )
            VALUES ( 0, 'entrance', 'entrance', 'n-1' );
      """ )
   conn.commit()

   yield conn

   conn.close()


def _scheduled_animal_times( conn: sqlite3.Connection ) -> tuple[ str | None, str | None ]:
   row = conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   return row[ 'START_TIME' ], row[ 'END_TIME' ]


def Test_ClearGuestItems_TestScheduledRows_ExpectClearedSchedules(
      schedule_clearer_conn: sqlite3.Connection ) -> None:
   ItineraryScheduleClearer.clear_guest_items( schedule_clearer_conn )

   start_time, end_time = _scheduled_animal_times( schedule_clearer_conn )
   attraction = schedule_clearer_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()
   event_count = schedule_clearer_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryEvent;' ).fetchone()
   walk_stop_count = schedule_clearer_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryWalkRouteStop;' ).fetchone()

   assert start_time is None
   assert end_time is None
   assert attraction is not None
   assert attraction[ 'START_TIME' ] is None
   assert attraction[ 'END_TIME' ] is None
   assert event_count is not None
   assert event_count[ 'COUNT' ] == 0
   assert walk_stop_count is not None
   assert walk_stop_count[ 'COUNT' ] == 1


def Test_ClearAll_TestScheduledRows_ExpectClearedSchedulesAndWalkRoute(
      schedule_clearer_conn: sqlite3.Connection ) -> None:
   ItineraryScheduleClearer.clear_all( schedule_clearer_conn )

   start_time, end_time = _scheduled_animal_times( schedule_clearer_conn )
   walk_stop_count = schedule_clearer_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryWalkRouteStop;' ).fetchone()

   assert start_time is None
   assert end_time is None
   assert walk_stop_count is not None
   assert walk_stop_count[ 'COUNT' ] == 0
