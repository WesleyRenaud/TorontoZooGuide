from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider


KANGAROO = 'Kangaroo'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'
VISIT_DATE = '2026-07-09'

SCHEDULE_PROVIDER_SCHEMA = """
PRAGMA foreign_keys=OFF;

CREATE TABLE WildEncounter (
   NAME             TEXT    NOT NULL PRIMARY KEY,
   MEETING_SPOT     TEXT    NOT NULL,
   LINK             TEXT    NOT NULL,
   MAXIMUM_DURATION INTEGER NOT NULL
);

CREATE TABLE WildEncounterMeetingSpot (
   NAME      TEXT  NOT NULL PRIMARY KEY,
   X_COORD   FLOAT NOT NULL,
   Y_COORD   FLOAT NOT NULL,
   REGION    TEXT  NOT NULL
);

CREATE TABLE WildEncounterSchedule (
   WILD_ENCOUNTER      TEXT NOT NULL,
   SCHEDULE_START_DATE DATE NOT NULL,
   SCHEDULE_END_DATE   DATE,
   MONDAY              BOOL NOT NULL DEFAULT 0,
   TUESDAY             BOOL NOT NULL DEFAULT 0,
   WEDNESDAY           BOOL NOT NULL DEFAULT 0,
   THURSDAY            BOOL NOT NULL DEFAULT 0,
   FRIDAY              BOOL NOT NULL DEFAULT 0,
   SATURDAY            BOOL NOT NULL DEFAULT 0,
   SUNDAY              BOOL NOT NULL DEFAULT 0,
   ENCOUNTER_TIME      TEXT NOT NULL,
   SCHEDULE_MESSAGE    TEXT,
   PRIMARY KEY (WILD_ENCOUNTER, ENCOUNTER_TIME, SCHEDULE_START_DATE)
);

CREATE TABLE WildEncounterCancellation (
   WILD_ENCOUNTER    TEXT NOT NULL,
   CANCELLATION_DATE DATE NOT NULL,
   ENCOUNTER_TIME    TEXT NOT NULL,
   PRIMARY KEY (WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME)
);
"""


@pytest.fixture
def schedule_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEDULE_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO WildEncounterMeetingSpot (
               NAME, X_COORD, Y_COORD, REGION
            ) VALUES ( ?, 0.0, 0.0, 'Eurasia Wilds' );
      """,
      ( 'Wild Encounter - Eurasia Meeting Spot', ),
   )
   conn.execute(
      """   INSERT INTO WildEncounter (
               NAME, MEETING_SPOT, LINK, MAXIMUM_DURATION
            ) VALUES ( ?, ?, ?, ? );
      """,
      (
         KANGAROO,
         'Wild Encounter - Eurasia Meeting Spot',
         'https://example.test/kangaroo',
         45,
      ),
   )
   conn.commit()

   yield conn

   conn.close()


def _insert_schedule_row(
      conn: sqlite3.Connection,
      *,
      start_date: str,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               ENCOUNTER_TIME
            ) VALUES ( ?, ?, ?, 1, 1, 1, 1, 1, 1, 1, ? );
      """,
      ( KANGAROO, start_date, end_date, KANGAROO_ENCOUNTER_TIME ),
   )


def Test_FetchScheduleRecords_TestExpiredAndActiveRows_ExpectOnlyActiveRowOnVisitDate(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-06-28',
      end_date='2026-07-05' )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-06',
      end_date=None )
   schedule_provider_conn.commit()

   records = WildEncounterScheduleProvider.fetch_schedule_records(
      schedule_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   assert records[ 0 ].name == KANGAROO
   assert records[ 0 ].schedule_start_date == '2026-07-06'
   assert records[ 0 ].encounter_time == KANGAROO_ENCOUNTER_TIME
