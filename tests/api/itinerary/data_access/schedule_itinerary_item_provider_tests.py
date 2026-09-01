from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from api.models.itinerary_event import ItineraryEvent
from api.shared.enums import ItineraryEventType


SCHEDULE_ITEM_SCHEMA = """
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

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'


@pytest.fixture
def schedule_item_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEDULE_ITEM_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, 0 );
      """,
      ( LION_SPECIES, LION_EXHIBIT ) )
   conn.execute(
      'INSERT INTO ItineraryAttraction ( ATTRACTION ) VALUES ( ? );',
      ( CAROUSEL, ) )
   conn.execute(
      'INSERT INTO ItineraryEvent ( EVENT_TYPE ) VALUES ( ? );',
      ( ItineraryEventType.LUNCH.value, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_InsertItineraryAnimalSchedule_TestNewAnimal_ExpectInserted(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   inserted = ScheduleItineraryItemProvider.insert_itinerary_animal_schedule(
      cur,
      species='Cheetah',
      exhibit=LION_EXHIBIT,
      start_time='10:00 AM',
      end_time='10:08 AM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'Cheetah', ),
   ).fetchone()

   assert inserted is True
   assert row is not None
   assert row[ 'START_TIME' ] == '10:00 AM'
   assert row[ 'END_TIME' ] == '10:08 AM'


def Test_UpdateItineraryAnimalSchedule_TestExistingAnimal_ExpectUpdatedTimes(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   updated = ScheduleItineraryItemProvider.update_itinerary_animal_schedule(
      cur,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time='11:00 AM',
      end_time='11:08 AM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION_SPECIES, ),
   ).fetchone()

   assert updated is True
   assert row is not None
   assert row[ 'START_TIME' ] == '11:00 AM'
   assert row[ 'END_TIME' ] == '11:08 AM'


def Test_UpdateItineraryAnimalCoverAndSchedule_TestExistingAnimal_ExpectCoveredFlag(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   updated = ScheduleItineraryItemProvider.update_itinerary_animal_cover_and_schedule(
      cur,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      covered_by_talk=True,
      start_time='3:00 PM',
      end_time='3:30 PM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME, COVERED_BY_TALK
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION_SPECIES, ),
   ).fetchone()

   assert updated is True
   assert row is not None
   assert row[ 'COVERED_BY_TALK' ] == 1
   assert row[ 'START_TIME' ] == '3:00 PM'


def Test_UpdateItineraryAttractionSchedule_TestExistingAttraction_ExpectUpdatedTimes(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   updated = ScheduleItineraryItemProvider.update_itinerary_attraction_schedule(
      cur,
      name=CAROUSEL,
      start_time='12:00 PM',
      end_time='12:20 PM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()

   assert updated is True
   assert row is not None
   assert row[ 'START_TIME' ] == '12:00 PM'
   assert row[ 'END_TIME' ] == '12:20 PM'


def Test_InsertItineraryEventSchedule_TestLunchEvent_ExpectInserted(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   ScheduleItineraryItemProvider.insert_itinerary_event_schedule(
      cur,
      ItineraryEvent(
         event_type=ItineraryEventType.DINNER,
         start_time='5:00 PM',
         end_time='5:40 PM' ) )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.DINNER.value, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '5:00 PM'
   assert row[ 'END_TIME' ] == '5:40 PM'


def Test_InsertItineraryGuardiansTalk_TestTalk_ExpectInserted(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   inserted = ScheduleItineraryItemProvider.insert_itinerary_guardians_talk(
      cur,
      talk_name='African Lion',
      start_time='2:00 PM',
      end_time='2:30 PM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = ?;
      """,
      ( 'African Lion', ),
   ).fetchone()

   assert inserted is True
   assert row is not None
   assert row[ 'START_TIME' ] == '2:00 PM'
   assert row[ 'IS_DELETED' ] == 0


def Test_InsertItineraryWildEncounter_TestEncounter_ExpectInserted(
      schedule_item_conn: sqlite3.Connection ) -> None:
   cur = schedule_item_conn.cursor()
   inserted = ScheduleItineraryItemProvider.insert_itinerary_wild_encounter(
      cur,
      wild_encounter_name='Giraffe',
      start_time='1:00 PM',
      end_time='1:30 PM' )
   schedule_item_conn.commit()
   cur.close()

   row = schedule_item_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( 'Giraffe', ),
   ).fetchone()

   assert inserted is True
   assert row is not None
   assert row[ 'START_TIME' ] == '1:00 PM'
   assert row[ 'END_TIME' ] == '1:30 PM'
