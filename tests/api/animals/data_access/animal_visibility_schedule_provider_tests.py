from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_visibility_schedule_provider import AnimalVisibilityScheduleProvider


SPECIES = 'Amur Tiger'
EXHIBIT = 'Eurasia Wilds'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
DAILY_START_TIME = '09:00'
DAILY_END_TIME = '11:00'
MESSAGE = 'Morning viewing only.'

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
def animal_visibility_schedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VISIBILITY_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def Test_SaveAnimalLimitedViewingSchedule_TestNewSchedule_ExpectPersistsRow(
      animal_visibility_schedule_conn: sqlite3.Connection ) -> None:
   assert AnimalVisibilityScheduleProvider.save_animal_limited_viewing_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message=MESSAGE ) is True

   row = animal_visibility_schedule_conn.execute(
      """   SELECT
               SPECIES,
               EXHIBIT,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               DAILY_START_TIME,
               DAILY_END_TIME,
               VIEWING_MESSAGE
            FROM AnimalVisibilitySchedule
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchone()

   assert tuple( row ) == (
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      DAILY_START_TIME,
      DAILY_END_TIME,
      MESSAGE,
   )


def Test_SaveAnimalLimitedViewingSchedule_TestExistingSchedule_ExpectUpdatesRow(
      animal_visibility_schedule_conn: sqlite3.Connection ) -> None:
   AnimalVisibilityScheduleProvider.save_animal_limited_viewing_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message=MESSAGE )

   assert AnimalVisibilityScheduleProvider.save_animal_limited_viewing_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date='2026-07-01',
      end_date='2026-07-15',
      daily_start_time='10:00',
      daily_end_time='12:00',
      message='Updated schedule.' ) is True

   row = animal_visibility_schedule_conn.execute(
      """   SELECT
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               DAILY_START_TIME,
               DAILY_END_TIME,
               VIEWING_MESSAGE
            FROM AnimalVisibilitySchedule
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchone()

   assert tuple( row ) == (
      '2026-07-01',
      '2026-07-15',
      '10:00',
      '12:00',
      'Updated schedule.',
   )


def Test_DeleteAnimalVisibilitySchedule_TestExistingSchedule_ExpectRemovesRow(
      animal_visibility_schedule_conn: sqlite3.Connection ) -> None:
   AnimalVisibilityScheduleProvider.save_animal_limited_viewing_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message=MESSAGE )

   assert AnimalVisibilityScheduleProvider.delete_animal_visibility_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT ) is True

   row = animal_visibility_schedule_conn.execute(
      """   SELECT 1
            FROM AnimalVisibilitySchedule
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchone()

   assert row is None


def Test_DeleteAnimalVisibilitySchedule_TestMissingSchedule_ExpectFalse(
      animal_visibility_schedule_conn: sqlite3.Connection ) -> None:
   assert AnimalVisibilityScheduleProvider.delete_animal_visibility_schedule(
      animal_visibility_schedule_conn,
      species=SPECIES,
      exhibit=EXHIBIT ) is False
