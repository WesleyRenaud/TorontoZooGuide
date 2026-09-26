from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.remove_itinerary_item_provider import RemoveItineraryItemProvider
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.shared.date_values import DateValues
from api.shared.enums import ItineraryEventType


REMOVE_PROVIDER_SCHEMA = """
CREATE TABLE ItineraryAnimal (
   SPECIES                 TEXT        NOT NULL,
   EXHIBIT                 TEXT        NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER     NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER     NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT
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

LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
CAROUSEL = 'Conservation Carousel'
GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
LUNCH_START_TIME = '12:00 PM'
LUNCH_DURATION_MINUTES = 30
LUNCH_END_TIME = DateValues.add_minutes_to_time(
   LUNCH_START_TIME,
   LUNCH_DURATION_MINUTES )


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
      ( LION_SPECIES, LION_EXHIBIT ) )
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
      ( ItineraryEventType.LUNCH.value, LUNCH_START_TIME, LUNCH_END_TIME ) )
   conn.commit()

   yield conn

   conn.close()


def Test_DeleteItineraryAnimal_TestAnimalRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   species = LION_SPECIES
   exhibit = LION_EXHIBIT
   cur = remove_provider_conn.cursor()

   RemoveItineraryItemProvider.delete_itinerary_animal(
      cur,
      species=species,
      exhibit=exhibit )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryAttraction_TestAttractionRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   name = CAROUSEL
   cur = remove_provider_conn.cursor()

   RemoveItineraryItemProvider.delete_itinerary_attraction(
      cur,
      name=name )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAttraction;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryGuardiansTalk_TestTalkRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   talk_name = GUARDIANS_TALK
   cur = remove_provider_conn.cursor()

   RemoveItineraryItemProvider.delete_itinerary_guardians_talk(
      cur,
      talk_name=talk_name )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryGuardiansTalk;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryWildEncounter_TestEncounterRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   wild_encounter = WILD_ENCOUNTER
   cur = remove_provider_conn.cursor()

   RemoveItineraryItemProvider.delete_itinerary_wild_encounter(
      cur,
      wild_encounter=wild_encounter )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryWildEncounter;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_DeleteItineraryEvent_TestLunchRow_ExpectRowRemoved(
      remove_provider_conn: sqlite3.Connection ) -> None:
   event_type = ItineraryEventType.LUNCH
   cur = remove_provider_conn.cursor()

   RemoveItineraryItemProvider.delete_itinerary_event(
      cur,
      event_type=event_type )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryEvent;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_ApplyViaRemover_TestAnimalKey_ExpectProviderDeletesRow(
      remove_provider_conn: sqlite3.Connection ) -> None:
   animal_key = AnimalScheduleItemKey(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT )
   cur = remove_provider_conn.cursor()

   ItineraryItemRemover.apply( cur, animal_key )
   remove_provider_conn.commit()
   cur.close()
   count = remove_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0
