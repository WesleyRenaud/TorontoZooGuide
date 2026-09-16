from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_visibility_schedule_exhibit_name_provider import AnimalVisibilityScheduleExhibitNameProvider


TODAY = '2026-09-16'
LION = 'African Lion'
TIGER = 'Amur Tiger'
GIRAFFE = 'Giraffe'
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
def visibility_schedule_exhibit_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VISIBILITY_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def _insert_schedule(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      start_date: str | None,
      end_date: str | None ) -> None:
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
         '09:00',
         '11:00',
         'Limited viewing.',
      ) )
   conn.commit()


def Test_FetchVisibilityScheduleExhibitNames_TestEmpty_ExpectEmptyList(
      visibility_schedule_exhibit_conn: sqlite3.Connection ) -> None:
   assert AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names(
      visibility_schedule_exhibit_conn,
      TODAY ) == []


def Test_FetchVisibilityScheduleExhibitNames_TestCurrentAndFuture_ExpectDistinctSortedExhibits(
      visibility_schedule_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      visibility_schedule_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_schedule(
      visibility_schedule_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      start_date='2026-10-01',
      end_date='2026-10-15' )
   _insert_schedule(
      visibility_schedule_exhibit_conn,
      species=GIRAFFE,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )

   assert AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names(
      visibility_schedule_exhibit_conn,
      TODAY ) == [ SAVANNA, EURASIA ]


def Test_FetchVisibilityScheduleExhibitNames_TestExpired_ExpectExcluded(
      visibility_schedule_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      visibility_schedule_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names(
      visibility_schedule_exhibit_conn,
      TODAY ) == []


def Test_FetchVisibilityScheduleExhibitNames_TestEndingToday_ExpectIncluded(
      visibility_schedule_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      visibility_schedule_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names(
      visibility_schedule_exhibit_conn,
      TODAY ) == [ SAVANNA ]
