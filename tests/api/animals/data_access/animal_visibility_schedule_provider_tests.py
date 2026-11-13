from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_visibility_schedule_provider import AnimalVisibilityScheduleProvider


LION = 'African Lion'
TIGER = 'Amur Tiger'
SAVANNA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'

ANIMAL_VISIBILITY_SCHEDULE_SCHEMA = """
CREATE TABLE AnimalVisibilitySchedule (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   SCHEDULE_START_DATE  TEXT,
   SCHEDULE_END_DATE    TEXT,
   DAILY_START_TIME     TEXT,
   DAILY_END_TIME       TEXT,
   VIEWING_MESSAGE      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""


@pytest.fixture
def visibility_schedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VISIBILITY_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def _insert_schedule(
      conn: sqlite3.Connection,
      species: str,
      exhibit: str,
      start_date: str | None,
      end_date: str | None,
      opens: str,
      closes: str,
      message: str ) -> None:
   conn.execute(
      """   INSERT INTO AnimalVisibilitySchedule (
               SPECIES,
               EXHIBIT,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               DAILY_START_TIME,
               DAILY_END_TIME,
               VIEWING_MESSAGE
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         start_date,
         end_date,
         opens,
         closes,
         message,
      ) )
   conn.commit()


def Test_FetchAnimalVisibilitySchedules_TestEmpty_ExpectEmptyList(
      visibility_schedule_conn: sqlite3.Connection ) -> None:
   schedules = AnimalVisibilityScheduleProvider.fetch_animal_visibility_schedules(
      visibility_schedule_conn )

   assert schedules == []


def Test_FetchAnimalVisibilitySchedules_TestOpenAndDated_ExpectBothRows(
      visibility_schedule_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      visibility_schedule_conn,
      TIGER,
      EURASIA,
      '2026-11-02',
      '2026-12-02',
      '10:00 AM',
      '2:00 PM',
      'Tiger hours.',
   )
   _insert_schedule(
      visibility_schedule_conn,
      LION,
      SAVANNA,
      None,
      None,
      '9:00 AM',
      '11:00 AM',
      'Lion hours.',
   )

   schedules = AnimalVisibilityScheduleProvider.fetch_animal_visibility_schedules(
      visibility_schedule_conn )

   assert [ ( item.species, item.exhibit ) for item in schedules ] == [
      ( LION, SAVANNA ),
      ( TIGER, EURASIA ),
   ]
   assert schedules[ 0 ].start_date == None
   assert schedules[ 0 ].end_date == None
   assert schedules[ 0 ].daily_start_time == '9:00 AM'
   assert schedules[ 0 ].daily_end_time == '11:00 AM'
   assert schedules[ 0 ].message == 'Lion hours.'
   assert schedules[ 1 ].start_date == '2026-11-02'
   assert schedules[ 1 ].end_date == '2026-12-02'
   assert schedules[ 1 ].message == 'Tiger hours.'
