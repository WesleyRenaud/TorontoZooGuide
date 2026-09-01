from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.save_itinerary_provider import SaveItineraryProvider
from api.models.wild_encounter_diff import WildEncounterDiff


SAVE_PROVIDER_SCHEMA = """
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
