from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.save_itinerary_provider import SaveItineraryProvider
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff


SAVE_PROVIDER_SCHEMA = """
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


@pytest.fixture
def save_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SAVE_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_SaveItineraryWildEncounters_Test24HourStartTime_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   wild_encounters = [
      WildEncounterDiff(
         name='Grizzly Bear',
         is_deleted=False,
         start_time='13:00',
         end_time='1:45 PM',
         meeting_spot='Americas Pavilion',
         link='https://example.com/grizzly' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, wild_encounters )
   save_provider_conn.commit()
   cur.close()

   encounter = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert encounter is not None
   assert dict( encounter ) == {
      'START_TIME': '1:00 PM',
      'END_TIME': '1:45 PM',
   }


def Test_SaveItineraryGuardiansTalks_TestScheduledTalk_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   guardians_talks = [
      GuardiansTalkDiff(
         name='African Lion',
         is_deleted=False,
         start_time='10:00',
         end_time='10:30' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_guardians_talks( cur, guardians_talks )
   save_provider_conn.commit()
   cur.close()

   talk = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = 'African Lion';
      """ ).fetchone()

   assert talk is not None
   assert dict( talk ) == {
      'START_TIME': '10:00 AM',
      'END_TIME': '10:30 AM',
      'IS_DELETED': 0,
   }


def Test_SaveItineraryWildEncounters_TestScheduledEncounter_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   wild_encounters = [
      WildEncounterDiff(
         name='African Rainforest',
         is_deleted=False,
         start_time='14:00',
         end_time='2:45 PM',
         meeting_spot='Rainforest Gate',
         link='african-rainforest' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, wild_encounters )
   save_provider_conn.commit()
   cur.close()

   encounter = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'African Rainforest';
      """ ).fetchone()

   assert encounter is not None
   assert dict( encounter ) == {
      'START_TIME': '2:00 PM',
      'END_TIME': '2:45 PM',
      'IS_DELETED': 0,
   }
