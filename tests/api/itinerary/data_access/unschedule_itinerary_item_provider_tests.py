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
"""

CAROUSEL = 'Conservation Carousel'


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
