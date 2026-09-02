from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.data_access.wild_encounter_provider import WildEncounterProvider


KANGAROO = 'Kangaroo'
OTTER = 'Otter'
KANGAROO_SPOT = 'Wild Encounter - Eurasia Meeting Spot'
OTTER_SPOT = 'Wild Encounter - Americas Meeting Spot'
LINK = 'https://example.test/kangaroo'
OTTER_LINK = 'https://example.test/otter'
MAXIMUM_DURATION = 45
OTTER_DURATION = 30
X_COORD = 1.5
Y_COORD = 2.5
REGION = 'Eurasia Wilds'
OTTER_REGION = 'Canadian Domain'

WILD_ENCOUNTER_PROVIDER_SCHEMA = """
PRAGMA foreign_keys=OFF;

CREATE TABLE WildEncounterMeetingSpot (
   NAME     TEXT  NOT NULL PRIMARY KEY,
   X_COORD  REAL  NOT NULL,
   Y_COORD  REAL  NOT NULL,
   REGION   TEXT  NOT NULL
);

CREATE TABLE WildEncounter (
   NAME             TEXT    NOT NULL PRIMARY KEY,
   MEETING_SPOT     TEXT    NOT NULL,
   LINK             TEXT    NOT NULL,
   MAXIMUM_DURATION INTEGER NOT NULL
);
"""


@pytest.fixture
def wild_encounter_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( WILD_ENCOUNTER_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_meeting_spot(
      conn: sqlite3.Connection,
      *,
      name: str,
      x_coord: float,
      y_coord: float,
      region: str ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounterMeetingSpot (
               NAME, X_COORD, Y_COORD, REGION
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( name, x_coord, y_coord, region ),
   )


def _insert_encounter(
      conn: sqlite3.Connection,
      *,
      name: str,
      meeting_spot: str,
      link: str,
      maximum_duration: int ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounter (
               NAME, MEETING_SPOT, LINK, MAXIMUM_DURATION
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( name, meeting_spot, link, maximum_duration ),
   )


def Test_FetchWildEncounterNames_TestEmpty_ExpectEmptyList(
      wild_encounter_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterProvider.fetch_wild_encounter_names(
      wild_encounter_provider_conn ) == []


def Test_FetchWildEncounterNames_TestPopulated_ExpectNames(
      wild_encounter_provider_conn: sqlite3.Connection ) -> None:
   _insert_meeting_spot(
      wild_encounter_provider_conn,
      name=KANGAROO_SPOT,
      x_coord=X_COORD,
      y_coord=Y_COORD,
      region=REGION )
   _insert_meeting_spot(
      wild_encounter_provider_conn,
      name=OTTER_SPOT,
      x_coord=3.0,
      y_coord=4.0,
      region=OTTER_REGION )
   _insert_encounter(
      wild_encounter_provider_conn,
      name=KANGAROO,
      meeting_spot=KANGAROO_SPOT,
      link=LINK,
      maximum_duration=MAXIMUM_DURATION )
   _insert_encounter(
      wild_encounter_provider_conn,
      name=OTTER,
      meeting_spot=OTTER_SPOT,
      link=OTTER_LINK,
      maximum_duration=OTTER_DURATION )
   wild_encounter_provider_conn.commit()

   names = WildEncounterProvider.fetch_wild_encounter_names(
      wild_encounter_provider_conn )

   assert set( names ) == { KANGAROO, OTTER }


def Test_FetchWildEncounterRecords_TestEmpty_ExpectEmptyList(
      wild_encounter_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterProvider.fetch_wild_encounter_records(
      wild_encounter_provider_conn ) == []


def Test_FetchWildEncounterRecords_TestJoinedMeetingSpot_ExpectMappedFields(
      wild_encounter_provider_conn: sqlite3.Connection ) -> None:
   _insert_meeting_spot(
      wild_encounter_provider_conn,
      name=KANGAROO_SPOT,
      x_coord=X_COORD,
      y_coord=Y_COORD,
      region=REGION )
   _insert_meeting_spot(
      wild_encounter_provider_conn,
      name=OTTER_SPOT,
      x_coord=3.0,
      y_coord=4.0,
      region=OTTER_REGION )
   _insert_encounter(
      wild_encounter_provider_conn,
      name=KANGAROO,
      meeting_spot=KANGAROO_SPOT,
      link=LINK,
      maximum_duration=MAXIMUM_DURATION )
   _insert_encounter(
      wild_encounter_provider_conn,
      name=OTTER,
      meeting_spot=OTTER_SPOT,
      link=OTTER_LINK,
      maximum_duration=OTTER_DURATION )
   wild_encounter_provider_conn.commit()

   records = WildEncounterProvider.fetch_wild_encounter_records(
      wild_encounter_provider_conn )
   by_name = { record.name: record for record in records }

   assert set( by_name ) == { KANGAROO, OTTER }
   assert by_name[ KANGAROO ].meeting_spot == KANGAROO_SPOT
   assert by_name[ KANGAROO ].link == LINK
   assert by_name[ KANGAROO ].maximum_duration == MAXIMUM_DURATION
   assert by_name[ KANGAROO ].x_coord == X_COORD
   assert by_name[ KANGAROO ].y_coord == Y_COORD
   assert by_name[ KANGAROO ].region == REGION
   assert by_name[ OTTER ].meeting_spot == OTTER_SPOT
   assert by_name[ OTTER ].region == OTTER_REGION
   assert by_name[ OTTER ].maximum_duration == OTTER_DURATION
