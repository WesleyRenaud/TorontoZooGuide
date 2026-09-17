from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.data_access.wild_encounter_schedule_name_provider import WildEncounterScheduleNameProvider


TODAY = '2026-09-16'
GIRAFFE = 'Giraffe Encounter'
KANGAROO = 'Kangaroo Encounter'

WILD_ENCOUNTER_SCHEDULE_SCHEMA = """
CREATE TABLE WildEncounterSchedule (
   WILD_ENCOUNTER      TEXT NOT NULL,
   SCHEDULE_START_DATE TEXT NOT NULL,
   SCHEDULE_END_DATE   TEXT,
   ENCOUNTER_TIME      TEXT NOT NULL,
   PRIMARY KEY ( WILD_ENCOUNTER, ENCOUNTER_TIME, SCHEDULE_START_DATE )
);
"""


@pytest.fixture
def wild_encounter_schedule_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( WILD_ENCOUNTER_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def _insert_schedule(
      conn: sqlite3.Connection,
      *,
      wild_encounter: str,
      start_date: str,
      end_date: str | None,
      encounter_time: str = '11:00 AM' ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ENCOUNTER_TIME
            )
            VALUES ( ?, ?, ?, ? );
      """,
      (
         wild_encounter,
         start_date,
         end_date,
         encounter_time,
      ) )
   conn.commit()


def Test_FetchScheduledWildEncounterNames_TestEmpty_ExpectEmptyList(
      wild_encounter_schedule_name_conn: sqlite3.Connection ) -> None:
   assert WildEncounterScheduleNameProvider.fetch_scheduled_wild_encounter_names(
      wild_encounter_schedule_name_conn,
      TODAY ) == []


def Test_FetchScheduledWildEncounterNames_TestCurrentAndFuture_ExpectDistinctSortedEncounters(
      wild_encounter_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=KANGAROO,
      start_date='2026-10-01',
      end_date='2026-10-15' )
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=GIRAFFE,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=GIRAFFE,
      start_date='2026-09-01',
      end_date='2026-09-30',
      encounter_time='2:00 PM' )
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=KANGAROO,
      start_date='2026-10-01',
      end_date=None,
      encounter_time='3:30 PM' )

   assert WildEncounterScheduleNameProvider.fetch_scheduled_wild_encounter_names(
      wild_encounter_schedule_name_conn,
      TODAY ) == [ GIRAFFE, KANGAROO ]


def Test_FetchScheduledWildEncounterNames_TestExpired_ExpectExcluded(
      wild_encounter_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=GIRAFFE,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert WildEncounterScheduleNameProvider.fetch_scheduled_wild_encounter_names(
      wild_encounter_schedule_name_conn,
      TODAY ) == []


def Test_FetchScheduledWildEncounterNames_TestEndingToday_ExpectExcluded(
      wild_encounter_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      wild_encounter_schedule_name_conn,
      wild_encounter=GIRAFFE,
      start_date='2026-09-01',
      end_date=TODAY )

   assert WildEncounterScheduleNameProvider.fetch_scheduled_wild_encounter_names(
      wild_encounter_schedule_name_conn,
      TODAY ) == []
