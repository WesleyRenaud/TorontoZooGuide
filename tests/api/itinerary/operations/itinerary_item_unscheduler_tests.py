from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.operations.itinerary_item_unscheduler import ItineraryItemUnscheduler
from api.shared.enums import ItineraryEventType


UNSCHEDULER_SCHEMA = """
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
LION_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)


@pytest.fixture
def unscheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
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
      ( ItineraryEventType.LUNCH.value, '12:00 PM', '12:40 PM' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Apply_TestAnimalKey_ExpectClearedSchedule(
      unscheduler_conn: sqlite3.Connection ) -> None:
   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply( cur, LION_KEY )
   unscheduler_conn.commit()
   cur.close()

   row = unscheduler_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_Apply_TestAttractionKey_ExpectClearedSchedule(
      unscheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row',
      lambda saved_itinerary, schedule_item_key: None )

   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply(
      cur,
      AttractionScheduleItemKey( name=CAROUSEL ) )
   unscheduler_conn.commit()
   cur.close()

   row = unscheduler_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_Apply_TestEventType_ExpectDeletedRow(
      unscheduler_conn: sqlite3.Connection ) -> None:
   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply( cur, ItineraryEventType.LUNCH )
   unscheduler_conn.commit()
   cur.close()

   count = unscheduler_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryEvent;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0
