from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from api.shared.enums import ItineraryEventType


UNSCHEDULE_SCHEMA = """
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

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
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
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'


@pytest.fixture
def unschedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULE_SCHEMA )
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
      ( 'African Lion', 'Africa Savanna', '10:00', '10:08' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( CAROUSEL, '11:00', '11:20' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:00', '12:40' ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def zoomobile_unschedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULE_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 1, ?, ?, ?, 1 );
      """,
      ( ZOOMOBILE, '10:00 AM', '11:15 AM', 'summer' ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 1, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, MAIN, CANADA, '10:00 AM', '10:20 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationRouteMarker (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               SEQUENCE,
               MARKER_ORDER,
               MARKER_ID
            )
            VALUES ( ?, 1, 0, 0, ? );
      """,
      ( ZOOMOBILE, 'm-a' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_ClearItineraryAnimalSchedule_TestScheduledAnimal_ExpectClearedTimes(
      unschedule_conn: sqlite3.Connection ) -> None:
   cur = unschedule_conn.cursor()
   UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
      cur,
      species='African Lion',
      exhibit='Africa Savanna' )
   unschedule_conn.commit()
   cur.close()

   row = unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME, COVERED_BY_TALK
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None
   assert row[ 'COVERED_BY_TALK' ] == 0


def Test_ClearItineraryAttractionSchedule_TestScheduledAttraction_ExpectClearedTimes(
      unschedule_conn: sqlite3.Connection ) -> None:
   cur = unschedule_conn.cursor()
   UnscheduleItineraryItemProvider.clear_itinerary_attraction_schedule(
      cur,
      name=CAROUSEL )
   unschedule_conn.commit()
   cur.close()

   row = unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_DeleteItineraryEventSchedule_TestScheduledEvent_ExpectRowDeleted(
      unschedule_conn: sqlite3.Connection ) -> None:
   cur = unschedule_conn.cursor()
   UnscheduleItineraryItemProvider.delete_itinerary_event_schedule(
      cur,
      event_type=ItineraryEventType.LUNCH )
   unschedule_conn.commit()
   cur.close()

   row = unschedule_conn.execute(
      """   SELECT EVENT_TYPE
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.LUNCH.value, ),
   ).fetchone()

   assert row is None


def Test_ClearItineraryTransportationSchedule_TestScheduledZoomobile_ExpectClearedTimesLegsAndMarkers(
      zoomobile_unschedule_conn: sqlite3.Connection ) -> None:
   cur = zoomobile_unschedule_conn.cursor()
   UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
      cur,
      name=ZOOMOBILE,
      added_as_attraction=True )
   zoomobile_unschedule_conn.commit()
   cur.close()

   transportation = zoomobile_unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   leg_count = zoomobile_unschedule_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   marker_count = zoomobile_unschedule_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryTransportationRouteMarker
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert transportation is not None
   assert transportation[ 'START_TIME' ] is None
   assert transportation[ 'END_TIME' ] is None
   assert transportation[ 'ROUTE' ] is None
   assert transportation[ 'BULK_TRANSIT_EVALUATED' ] == 0
   assert leg_count is not None
   assert leg_count[ 'COUNT' ] == 0
   assert marker_count is not None
   assert marker_count[ 'COUNT' ] == 0
