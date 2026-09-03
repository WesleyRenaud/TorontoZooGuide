from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.remove_itinerary_item_provider import RemoveItineraryItemProvider
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.shared.enums import ItineraryEventType


REMOVE_PROVIDER_SCHEMA = """
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

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);
"""

CAROUSEL = 'Conservation Carousel'
GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'


@pytest.fixture
def remove_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( REMOVE_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, NULL );
      """,
      ( 'African Lion', 'Africa Savanna' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction ( ATTRACTION )
            VALUES ( ? );
      """,
      ( CAROUSEL, ) )
   conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk ( TALK_NAME )
            VALUES ( ? );
      """,
      ( GUARDIANS_TALK, ) )
   conn.execute(
      """   INSERT INTO ItineraryWildEncounter ( WILD_ENCOUNTER )
            VALUES ( ? );
      """,
      ( WILD_ENCOUNTER, ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:00 PM', '12:30 PM' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_DeleteItineraryAnimal_TestAnimalRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   cur = remove_provider_conn.cursor()
   RemoveItineraryItemProvider.delete_itinerary_animal(
      cur,
      species='African Lion',
      exhibit='Africa Savanna' )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryAttraction_TestAttractionRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   cur = remove_provider_conn.cursor()
   RemoveItineraryItemProvider.delete_itinerary_attraction(
      cur,
      name=CAROUSEL )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAttraction;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryGuardiansTalk_TestTalkRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   cur = remove_provider_conn.cursor()
   RemoveItineraryItemProvider.delete_itinerary_guardians_talk(
      cur,
      talk_name=GUARDIANS_TALK )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryGuardiansTalk;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryWildEncounter_TestEncounterRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   cur = remove_provider_conn.cursor()
   RemoveItineraryItemProvider.delete_itinerary_wild_encounter(
      cur,
      wild_encounter=WILD_ENCOUNTER )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryWildEncounter;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryEvent_TestLunchRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   cur = remove_provider_conn.cursor()
   RemoveItineraryItemProvider.delete_itinerary_event(
      cur,
      event_type=ItineraryEventType.LUNCH )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryEvent;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_ApplyViaRemover_TestAnimalKey_ExpectProviderDeletesRow(
      remove_provider_conn: sqlite3.Connection ) -> None:

   cur = remove_provider_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      AnimalScheduleItemKey(
         species='African Lion',
         exhibit='Africa Savanna',
      ) )
   remove_provider_conn.commit()
   cur.close()

   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0
