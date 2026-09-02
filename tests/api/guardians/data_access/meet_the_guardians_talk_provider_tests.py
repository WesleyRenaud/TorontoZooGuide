from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.meet_the_guardians_talk_provider import MeetTheGuardiansTalkProvider


MEET_THE_GUARDIANS_TALK_PROVIDER_SCHEMA = """
CREATE TABLE MeetTheGuardiansTalk (
   NAME               TEXT NOT NULL,
   LOCATION           TEXT,
   X_COORD            REAL NOT NULL,
   Y_COORD            REAL NOT NULL,
   MAXIMUM_DURATION   INTEGER,
   PRIMARY KEY ( NAME, LOCATION )
);
"""

PENGUIN_TALK = 'African Penguin'
GORILLA_TALK = 'Western Lowland Gorilla'
LION_TALK = 'African Lion'
SAVANNA = 'Africa Savanna'
RAINFOREST = 'African Rainforest Pavilion'


@pytest.fixture
def meet_the_guardians_talk_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( MEET_THE_GUARDIANS_TALK_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_talk(
      conn: sqlite3.Connection,
      *,
      name: str,
      location: str | None,
      x_coord: float,
      y_coord: float,
      maximum_duration: int | None ) -> None:
   conn.execute(
      """   INSERT INTO MeetTheGuardiansTalk (
               NAME,
               LOCATION,
               X_COORD,
               Y_COORD,
               MAXIMUM_DURATION
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( name, location, x_coord, y_coord, maximum_duration ),
   )


def Test_FetchGuardiansTalkLocations_TestEmpty_ExpectEmptyList(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   assert MeetTheGuardiansTalkProvider.fetch_guardians_talk_locations(
      meet_the_guardians_talk_provider_conn ) == []


def Test_FetchGuardiansTalkLocations_TestDistinctOrderedAndNullFiltered_ExpectLocations(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=PENGUIN_TALK,
      location=SAVANNA,
      x_coord=1.0,
      y_coord=2.0,
      maximum_duration=20 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=LION_TALK,
      location=SAVANNA,
      x_coord=3.0,
      y_coord=4.0,
      maximum_duration=15 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=GORILLA_TALK,
      location=RAINFOREST,
      x_coord=5.0,
      y_coord=6.0,
      maximum_duration=25 )
   # SQLite allows one NULL primary-key component; use a distinct name.
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name='Unlocated Talk',
      location=None,
      x_coord=0.0,
      y_coord=0.0,
      maximum_duration=None )
   meet_the_guardians_talk_provider_conn.commit()

   locations = MeetTheGuardiansTalkProvider.fetch_guardians_talk_locations(
      meet_the_guardians_talk_provider_conn )

   assert locations == [ SAVANNA, RAINFOREST ]


def Test_FetchGuardiansTalkNames_TestEmpty_ExpectEmptyList(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   assert MeetTheGuardiansTalkProvider.fetch_guardians_talk_names(
      meet_the_guardians_talk_provider_conn ) == []


def Test_FetchGuardiansTalkNames_TestPopulated_ExpectNames(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=PENGUIN_TALK,
      location=SAVANNA,
      x_coord=1.0,
      y_coord=2.0,
      maximum_duration=20 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=GORILLA_TALK,
      location=RAINFOREST,
      x_coord=5.0,
      y_coord=6.0,
      maximum_duration=25 )
   meet_the_guardians_talk_provider_conn.commit()

   names = MeetTheGuardiansTalkProvider.fetch_guardians_talk_names(
      meet_the_guardians_talk_provider_conn )

   assert set( names ) == { PENGUIN_TALK, GORILLA_TALK }


def Test_FetchGuardiansTalkNamesAtLocation_TestMatchingLocation_ExpectNames(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=PENGUIN_TALK,
      location=SAVANNA,
      x_coord=1.0,
      y_coord=2.0,
      maximum_duration=20 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=LION_TALK,
      location=SAVANNA,
      x_coord=3.0,
      y_coord=4.0,
      maximum_duration=15 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=GORILLA_TALK,
      location=RAINFOREST,
      x_coord=5.0,
      y_coord=6.0,
      maximum_duration=25 )
   meet_the_guardians_talk_provider_conn.commit()

   names = MeetTheGuardiansTalkProvider.fetch_guardians_talk_names_at_location(
      meet_the_guardians_talk_provider_conn,
      SAVANNA )

   assert set( names ) == { PENGUIN_TALK, LION_TALK }


def Test_FetchGuardiansTalkNamesAtLocation_TestUnknownLocation_ExpectEmptyList(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=PENGUIN_TALK,
      location=SAVANNA,
      x_coord=1.0,
      y_coord=2.0,
      maximum_duration=20 )
   meet_the_guardians_talk_provider_conn.commit()

   assert MeetTheGuardiansTalkProvider.fetch_guardians_talk_names_at_location(
      meet_the_guardians_talk_provider_conn,
      'Missing Location' ) == []


def Test_FetchMeetTheGuardiansTalkRecords_TestEmpty_ExpectEmptyList(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   assert MeetTheGuardiansTalkProvider.fetch_meet_the_guardians_talk_records(
      meet_the_guardians_talk_provider_conn ) == []


def Test_FetchMeetTheGuardiansTalkRecords_TestPopulated_ExpectMappedFields(
      meet_the_guardians_talk_provider_conn: sqlite3.Connection ) -> None:
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=PENGUIN_TALK,
      location=SAVANNA,
      x_coord=1.0,
      y_coord=2.0,
      maximum_duration=20 )
   _insert_talk(
      meet_the_guardians_talk_provider_conn,
      name=GORILLA_TALK,
      location=RAINFOREST,
      x_coord=5.0,
      y_coord=6.0,
      maximum_duration=None )
   meet_the_guardians_talk_provider_conn.commit()

   records = MeetTheGuardiansTalkProvider.fetch_meet_the_guardians_talk_records(
      meet_the_guardians_talk_provider_conn )
   by_name = { record.name: record for record in records }

   assert set( by_name ) == { PENGUIN_TALK, GORILLA_TALK }
   assert by_name[ PENGUIN_TALK ].location == SAVANNA
   assert by_name[ PENGUIN_TALK ].x_coord == 1.0
   assert by_name[ PENGUIN_TALK ].y_coord == 2.0
   assert by_name[ PENGUIN_TALK ].maximum_duration == 20
   assert by_name[ GORILLA_TALK ].location == RAINFOREST
   assert by_name[ GORILLA_TALK ].maximum_duration is None
