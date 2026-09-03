from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.data_access.wild_encounter_meeting_spot_loop_pin_provider import WildEncounterMeetingSpotLoopPinProvider
from api.wild_encounters.data_access.wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord

KANGAROO_SPOT = 'Wild Encounter - Eurasia Meeting Spot'
OTTER_SPOT = 'Wild Encounter - Americas Meeting Spot'
UNPINNED_SPOT = 'Wild Encounter - Unpinned Meeting Spot'
EURASIA_LOOP = 'eurasia'
AMERICAS_LOOP = 'americas'

MEETING_SPOT_LOOP_PIN_SCHEMA = """
CREATE TABLE WildEncounterMeetingSpot (
   NAME                     TEXT NOT NULL PRIMARY KEY,
   X_COORD                  REAL NOT NULL,
   Y_COORD                  REAL NOT NULL,
   LOOP_ID                  TEXT,
   LOOP_VIEWING_SPOT_INDEX  INTEGER,
   REGION                   TEXT NOT NULL
);
"""

@pytest.fixture
def meeting_spot_loop_pin_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( MEETING_SPOT_LOOP_PIN_SCHEMA )

   yield conn

   conn.close()

def _insert_meeting_spot(
      conn: sqlite3.Connection,
      *,
      name: str,
      loop_id: str | None,
      loop_viewing_spot_index: int | None ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounterMeetingSpot (
               NAME,
               X_COORD,
               Y_COORD,
               LOOP_ID,
               LOOP_VIEWING_SPOT_INDEX,
               REGION
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      ( name, 1.0, 2.0, loop_id, loop_viewing_spot_index, 'Eurasia Wilds' ),
   )

def Test_FetchMeetingSpotLoopPinsByName_TestEmpty_ExpectEmptyDict(
      meeting_spot_loop_pin_conn: sqlite3.Connection ) -> None:
   assert WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name(
      meeting_spot_loop_pin_conn ) == {}

def Test_FetchMeetingSpotLoopPinsByName_TestPinnedAndUnpinned_ExpectPinnedOnly(
      meeting_spot_loop_pin_conn: sqlite3.Connection ) -> None:
   _insert_meeting_spot(
      meeting_spot_loop_pin_conn,
      name=KANGAROO_SPOT,
      loop_id=EURASIA_LOOP,
      loop_viewing_spot_index=2 )
   _insert_meeting_spot(
      meeting_spot_loop_pin_conn,
      name=OTTER_SPOT,
      loop_id=AMERICAS_LOOP,
      loop_viewing_spot_index=0 )
   _insert_meeting_spot(
      meeting_spot_loop_pin_conn,
      name=UNPINNED_SPOT,
      loop_id=None,
      loop_viewing_spot_index=None )

   pins = WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name(
      meeting_spot_loop_pin_conn )

   assert pins == {
      KANGAROO_SPOT: WildEncounterMeetingSpotLoopPinRecord(
         name=KANGAROO_SPOT,
         loop_id=EURASIA_LOOP,
         loop_viewing_spot_index=2 ),
      OTTER_SPOT: WildEncounterMeetingSpotLoopPinRecord(
         name=OTTER_SPOT,
         loop_id=AMERICAS_LOOP,
         loop_viewing_spot_index=0 ),
   }
