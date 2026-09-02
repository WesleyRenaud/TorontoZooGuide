from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.data_access.wild_encounter_schedule_conflict_record import WildEncounterScheduleConflictRecord
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from api.wild_encounters.scheduling.wild_encounter_schedule_end_input import WildEncounterScheduleEndInput
from api.wild_encounters.scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput


KANGAROO = 'Kangaroo'
MEETING_SPOT = 'Wild Encounter - Eurasia Meeting Spot'
LINK = 'https://example.test/kangaroo'
MAXIMUM_DURATION = 45
X_COORD = 0.0
Y_COORD = 0.0
REGION = 'Eurasia Wilds'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'
SECOND_ENCOUNTER_TIME = '11:00 AM'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
VISIT_DATE = '2026-07-09'
MESSAGE = 'Summer encounter hours.'

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
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( MEETING_SPOT, X_COORD, Y_COORD, REGION ),
   )
   conn.execute(
      """   INSERT INTO WildEncounter (
               NAME, MEETING_SPOT, LINK, MAXIMUM_DURATION
            ) VALUES ( ?, ?, ?, ? );
      """,
      (
         KANGAROO,
         MEETING_SPOT,
         LINK,
         MAXIMUM_DURATION,
      ),
   )
   conn.commit()

   yield conn

   conn.close()


def _schedule_input(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      encounter_time: str = KANGAROO_ENCOUNTER_TIME,
      monday: bool = True,
      tuesday: bool = True,
      wednesday: bool = True,
      thursday: bool = True,
      friday: bool = True,
      saturday: bool = True,
      sunday: bool = True,
      message: str = MESSAGE ) -> WildEncounterScheduleInput:
   return WildEncounterScheduleInput(
      wild_encounter=KANGAROO,
      start_date=start_date,
      end_date=end_date,
      encounter_time=encounter_time,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      message=message )


def _conflict_record(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      encounter_time: str = KANGAROO_ENCOUNTER_TIME ) -> (
         WildEncounterScheduleConflictRecord ):
   return WildEncounterScheduleConflictRecord(
      wild_encounter=KANGAROO,
      encounter_time=encounter_time,
      schedule_start_date=start_date,
      schedule_end_date=end_date,
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      message=MESSAGE )


def _insert_schedule_row(
      conn: sqlite3.Connection,
      *,
      start_date: str,
      end_date: str | None,
      encounter_time: str = KANGAROO_ENCOUNTER_TIME,
      message: str | None = MESSAGE ) -> None:
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
               ENCOUNTER_TIME,
               SCHEDULE_MESSAGE
            ) VALUES ( ?, ?, ?, 1, 1, 1, 1, 1, 1, 1, ?, ? );
      """,
      ( KANGAROO, start_date, end_date, encounter_time, message ),
   )


def _fetch_schedule_row(
      conn: sqlite3.Connection,
      *,
      start_date: str,
      encounter_time: str = KANGAROO_ENCOUNTER_TIME ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT
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
               ENCOUNTER_TIME,
               SCHEDULE_MESSAGE
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?
               AND ENCOUNTER_TIME = ?
               AND SCHEDULE_START_DATE = ?;
      """,
      ( KANGAROO, encounter_time, start_date ) ).fetchone()


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
   assert not records[ 0 ].is_cancelled


def Test_FetchScheduleRecords_TestCancellationOnVisitDate_ExpectIsCancelledTrue(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-06',
      end_date=None )
   schedule_provider_conn.execute(
      """   INSERT INTO WildEncounterCancellation (
               WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME
            ) VALUES ( ?, ?, ? );
      """,
      ( KANGAROO, VISIT_DATE, KANGAROO_ENCOUNTER_TIME ),
   )
   schedule_provider_conn.commit()

   records = WildEncounterScheduleProvider.fetch_schedule_records(
      schedule_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   assert records[ 0 ].is_cancelled


def Test_FetchScheduleRecordsForOccurrences_TestMatchingEncounter_ExpectOrderedRecords(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=KANGAROO_ENCOUNTER_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=SECOND_ENCOUNTER_TIME )
   schedule_provider_conn.commit()

   records = WildEncounterScheduleProvider.fetch_schedule_records_for_occurrences(
      schedule_provider_conn,
      KANGAROO )

   assert [ record.encounter_time for record in records ] == [
      SECOND_ENCOUNTER_TIME,
      KANGAROO_ENCOUNTER_TIME,
   ]
   assert all( not record.is_cancelled for record in records )


def Test_FetchScheduleTimes_TestCoveringDate_ExpectDistinctOrderedTimes(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=KANGAROO_ENCOUNTER_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=SECOND_ENCOUNTER_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-01',
      end_date='2026-07-31',
      encounter_time='4:00 PM' )
   schedule_provider_conn.commit()

   times = WildEncounterScheduleProvider.fetch_schedule_times(
      schedule_provider_conn,
      KANGAROO,
      '2026-06-15' )

   assert times == [ SECOND_ENCOUNTER_TIME, KANGAROO_ENCOUNTER_TIME ]


def Test_ScheduleOverlapsExistingSchedule_TestOverlappingDates_ExpectTrue(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   assert WildEncounterScheduleProvider.schedule_overlaps_existing_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15' ) ) is True


def Test_ScheduleOverlapsExistingSchedule_TestNonOverlappingDates_ExpectFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   assert WildEncounterScheduleProvider.schedule_overlaps_existing_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-07-01',
         end_date='2026-07-31' ) ) is False


def Test_FetchScheduleConflicts_TestOverlappingSchedule_ExpectConflictRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   conflicts = WildEncounterScheduleProvider.fetch_schedule_conflicts(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15' ) )

   assert len( conflicts ) == 1
   assert conflicts[ 0 ].wild_encounter == KANGAROO
   assert conflicts[ 0 ].schedule_start_date == START_DATE
   assert conflicts[ 0 ].encounter_time == KANGAROO_ENCOUNTER_TIME
   assert conflicts[ 0 ].message == MESSAGE


def Test_FetchScheduleConflicts_TestNonOverlappingSchedule_ExpectEmpty(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   conflicts = WildEncounterScheduleProvider.fetch_schedule_conflicts(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-07-01',
         end_date='2026-07-31' ) )

   assert conflicts == []


def Test_DeleteSchedule_TestExistingSchedule_ExpectRemovesRow(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   WildEncounterScheduleProvider.delete_schedule(
      schedule_provider_conn,
      _conflict_record() )
   schedule_provider_conn.commit()

   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE ) is None


def Test_UpdateScheduleDates_TestExistingSchedule_ExpectUpdatesDates(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   WildEncounterScheduleProvider.update_schedule_dates(
      schedule_provider_conn,
      _conflict_record(),
      '2026-07-01',
      '2026-07-31' )
   schedule_provider_conn.commit()

   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE ) is None

   row = _fetch_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-01' )

   assert row is not None
   assert row[ 'SCHEDULE_START_DATE' ] == '2026-07-01'
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-07-31'
   assert row[ 'SCHEDULE_MESSAGE' ] == MESSAGE


def Test_InsertCopiedSchedule_TestExistingSchedule_ExpectInsertsCopy(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=END_DATE )
   schedule_provider_conn.commit()

   WildEncounterScheduleProvider.insert_copied_schedule(
      schedule_provider_conn,
      _conflict_record(),
      '2026-08-01',
      '2026-08-31' )
   schedule_provider_conn.commit()

   row = _fetch_schedule_row(
      schedule_provider_conn,
      start_date='2026-08-01' )

   assert tuple( row ) == (
      KANGAROO,
      '2026-08-01',
      '2026-08-31',
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      KANGAROO_ENCOUNTER_TIME,
      MESSAGE,
   )
   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE ) is not None


def Test_InsertOrUpdateSchedule_TestSameStartDate_ExpectUpdatesRow(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   WildEncounterScheduleProvider.insert_or_update_schedule(
      schedule_provider_conn,
      _schedule_input() )
   schedule_provider_conn.commit()

   WildEncounterScheduleProvider.insert_or_update_schedule(
      schedule_provider_conn,
      _schedule_input(
         end_date='2026-07-15',
         saturday=False,
         sunday=False,
         message='Updated encounter hours.' ) )
   schedule_provider_conn.commit()

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert tuple( row ) == (
      KANGAROO,
      START_DATE,
      '2026-07-15',
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      KANGAROO_ENCOUNTER_TIME,
      'Updated encounter hours.',
   )


def Test_SaveSchedule_TestNewSchedule_ExpectPersistsAndReturnsTrue(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input() ) is True

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert tuple( row ) == (
      KANGAROO,
      START_DATE,
      END_DATE,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      KANGAROO_ENCOUNTER_TIME,
      MESSAGE,
   )


def Test_SaveSchedule_TestOverlappingSchedule_ExpectReturnsFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   WildEncounterScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input() )

   assert WildEncounterScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Overlap.' ) ) is False

   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date='2026-06-15' ) is None


def Test_SaveScheduleEnd_TestCoveringSchedule_ExpectUpdatesEndDate(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE,
      end_date=None )
   schedule_provider_conn.commit()

   assert WildEncounterScheduleProvider.save_schedule_end(
      schedule_provider_conn,
      WildEncounterScheduleEndInput(
         wild_encounter=KANGAROO,
         schedule_end_date='2026-06-20',
         encounter_time=KANGAROO_ENCOUNTER_TIME ) ) is True

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert row is not None
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-06-20'


def Test_SaveScheduleEnd_TestNoMatchingSchedule_ExpectReturnsFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterScheduleProvider.save_schedule_end(
      schedule_provider_conn,
      WildEncounterScheduleEndInput(
         wild_encounter=KANGAROO,
         schedule_end_date='2026-06-20',
         encounter_time=KANGAROO_ENCOUNTER_TIME ) ) is False
