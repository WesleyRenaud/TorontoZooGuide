from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.scheduling.guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from api.guardians.scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput


TALK_NAME = 'African Lion'
LOCATION = 'Africa Savanna'
X_COORD = 1.5
Y_COORD = 2.5
MAXIMUM_DURATION = 20
TALK_TIME = '11:00 AM'
SECOND_TALK_TIME = '2:00 PM'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
VISIT_DATE = '2026-06-15'
MESSAGE = 'Summer talk hours.'

SCHEDULE_PROVIDER_SCHEMA = """
PRAGMA foreign_keys=OFF;

CREATE TABLE MeetTheGuardiansTalk (
   NAME             TEXT    NOT NULL,
   LOCATION         TEXT    NOT NULL,
   X_COORD          FLOAT   NOT NULL,
   Y_COORD          FLOAT   NOT NULL,
   MAXIMUM_DURATION INTEGER NOT NULL,
   PRIMARY KEY ( NAME, LOCATION )
);

CREATE TABLE GuardiansTalkSchedule (
   TALK_NAME           TEXT NOT NULL,
   LOCATION            TEXT NOT NULL,
   SCHEDULE_START_DATE DATE NOT NULL,
   SCHEDULE_END_DATE   DATE,
   MONDAY              BOOL NOT NULL DEFAULT 0,
   TUESDAY             BOOL NOT NULL DEFAULT 0,
   WEDNESDAY           BOOL NOT NULL DEFAULT 0,
   THURSDAY            BOOL NOT NULL DEFAULT 0,
   FRIDAY              BOOL NOT NULL DEFAULT 0,
   SATURDAY            BOOL NOT NULL DEFAULT 0,
   SUNDAY              BOOL NOT NULL DEFAULT 0,
   TALK_TIME           TEXT NOT NULL,
   SCHEDULE_MESSAGE    TEXT,
   PRIMARY KEY ( TALK_NAME, LOCATION, TALK_TIME, SCHEDULE_START_DATE )
);

CREATE TABLE GuardiansTalkCancellation (
   TALK_NAME         TEXT NOT NULL,
   LOCATION          TEXT NOT NULL,
   CANCELLATION_DATE DATE NOT NULL,
   TALK_TIME         TEXT NOT NULL,
   PRIMARY KEY ( TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME )
);
"""


@pytest.fixture
def schedule_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEDULE_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO MeetTheGuardiansTalk (
               NAME, LOCATION, X_COORD, Y_COORD, MAXIMUM_DURATION
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( TALK_NAME, LOCATION, X_COORD, Y_COORD, MAXIMUM_DURATION ),
   )
   conn.commit()

   yield conn

   conn.close()


def _schedule_input(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      talk_time: str = TALK_TIME,
      monday: bool = True,
      tuesday: bool = True,
      wednesday: bool = True,
      thursday: bool = True,
      friday: bool = True,
      saturday: bool = False,
      sunday: bool = False,
      message: str = MESSAGE ) -> GuardiansTalkScheduleInput:
   return GuardiansTalkScheduleInput(
      talk_name=TALK_NAME,
      location=LOCATION,
      start_date=start_date,
      end_date=end_date,
      talk_time=talk_time,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      message=message )


def _schedule_record(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      talk_time: str = TALK_TIME ) -> GuardiansTalkScheduleRecord:
   return GuardiansTalkScheduleRecord(
      name=TALK_NAME,
      location=LOCATION,
      x_coord=X_COORD,
      y_coord=Y_COORD,
      maximum_duration=MAXIMUM_DURATION,
      schedule_start_date=start_date,
      schedule_end_date=end_date,
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=False,
      sunday=False,
      talk_time=talk_time )


def _insert_schedule_row(
      conn: sqlite3.Connection,
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      talk_time: str = TALK_TIME,
      monday: int = 1,
      tuesday: int = 1,
      wednesday: int = 1,
      thursday: int = 1,
      friday: int = 1,
      saturday: int = 0,
      sunday: int = 0,
      message: str | None = MESSAGE ) -> None:
   conn.execute(
      """   INSERT INTO GuardiansTalkSchedule (
               TALK_NAME,
               LOCATION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               TALK_TIME,
               SCHEDULE_MESSAGE
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         TALK_NAME,
         LOCATION,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         talk_time,
         message,
      ),
   )


def _fetch_schedule_row(
      conn: sqlite3.Connection,
      *,
      start_date: str,
      talk_time: str = TALK_TIME ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT
               TALK_NAME,
               LOCATION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               TALK_TIME,
               SCHEDULE_MESSAGE
            FROM GuardiansTalkSchedule
            WHERE TALK_NAME = ?
               AND LOCATION = ?
               AND TALK_TIME = ?
               AND SCHEDULE_START_DATE = ?;
      """,
      ( TALK_NAME, LOCATION, talk_time, start_date ) ).fetchone()


def Test_FetchScheduleRecords_TestActiveSchedule_ExpectMappedRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   records = GuardiansTalkScheduleProvider.fetch_schedule_records(
      schedule_provider_conn )

   assert len( records ) == 1
   assert records[ 0 ] == _schedule_record()


def Test_FetchScheduleRecordsForTalk_TestMatchingTalk_ExpectOrderedRecords(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      talk_time=SECOND_TALK_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      talk_time=TALK_TIME )
   schedule_provider_conn.commit()

   records = GuardiansTalkScheduleProvider.fetch_schedule_records_for_talk(
      schedule_provider_conn,
      TALK_NAME,
      LOCATION )

   assert [ record.talk_time for record in records ] == [
      TALK_TIME,
      SECOND_TALK_TIME,
   ]


def Test_FetchScheduleRecordsForOccurrences_TestMatchingTalk_ExpectSameAsForTalk(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   for_talk = GuardiansTalkScheduleProvider.fetch_schedule_records_for_talk(
      schedule_provider_conn,
      TALK_NAME,
      LOCATION )
   for_occurrences = (
      GuardiansTalkScheduleProvider.fetch_schedule_records_for_occurrences(
         schedule_provider_conn,
         TALK_NAME,
         LOCATION )
   )

   assert for_occurrences == for_talk


def Test_FetchScheduleRecordsCoveringDate_TestDateInsideRange_ExpectRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-01',
      end_date='2026-07-31' )
   schedule_provider_conn.commit()

   records = GuardiansTalkScheduleProvider.fetch_schedule_records_covering_date(
      schedule_provider_conn,
      talk_name=TALK_NAME,
      location=LOCATION,
      talk_time=TALK_TIME,
      occurrence_date=VISIT_DATE )

   assert len( records ) == 1
   assert records[ 0 ].schedule_start_date == START_DATE


def Test_FetchScheduleRecordsCoveringDate_TestOpenEndedSchedule_ExpectRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-06-01',
      end_date=None )
   schedule_provider_conn.commit()

   records = GuardiansTalkScheduleProvider.fetch_schedule_records_covering_date(
      schedule_provider_conn,
      talk_name=TALK_NAME,
      location=LOCATION,
      talk_time=TALK_TIME,
      occurrence_date='2026-12-01' )

   assert len( records ) == 1
   assert records[ 0 ].schedule_end_date is None


def Test_FetchDayScheduleRecordsFromSchedule_TestNoCancellation_ExpectRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   records = (
      GuardiansTalkScheduleProvider.fetch_day_schedule_records_from_schedule(
         schedule_provider_conn,
         VISIT_DATE )
   )

   assert len( records ) == 1
   assert records[ 0 ].name == TALK_NAME
   assert records[ 0 ].talk_time == TALK_TIME


def Test_FetchDayScheduleRecordsFromSchedule_TestWithCancellation_ExpectEmpty(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.execute(
      """   INSERT INTO GuardiansTalkCancellation (
               TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( TALK_NAME, LOCATION, VISIT_DATE, TALK_TIME ),
   )
   schedule_provider_conn.commit()

   records = (
      GuardiansTalkScheduleProvider.fetch_day_schedule_records_from_schedule(
         schedule_provider_conn,
         VISIT_DATE )
   )

   assert records == []


def Test_FetchScheduleTimes_TestCoveringDate_ExpectDistinctOrderedTimes(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      talk_time=SECOND_TALK_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      talk_time=TALK_TIME )
   _insert_schedule_row(
      schedule_provider_conn,
      start_date='2026-07-01',
      end_date='2026-07-31',
      talk_time='4:00 PM' )
   schedule_provider_conn.commit()

   times = GuardiansTalkScheduleProvider.fetch_schedule_times(
      schedule_provider_conn,
      TALK_NAME,
      LOCATION,
      VISIT_DATE )

   assert times == [ TALK_TIME, SECOND_TALK_TIME ]


def Test_ScheduleOverlapsExistingSchedule_TestOverlappingDates_ExpectTrue(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   assert GuardiansTalkScheduleProvider.schedule_overlaps_existing_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15' ) ) is True


def Test_ScheduleOverlapsExistingSchedule_TestNonOverlappingDates_ExpectFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   assert GuardiansTalkScheduleProvider.schedule_overlaps_existing_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-07-01',
         end_date='2026-07-31' ) ) is False


def Test_SaveSchedule_TestNewSchedule_ExpectPersistsAndReturnsTrue(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input() ) is True

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert tuple( row ) == (
      TALK_NAME,
      LOCATION,
      START_DATE,
      END_DATE,
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      TALK_TIME,
      MESSAGE,
   )


def Test_SaveSchedule_TestOverlappingSchedule_ExpectReturnsFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   GuardiansTalkScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input() )

   assert GuardiansTalkScheduleProvider.save_schedule(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Overlap.' ) ) is False

   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date='2026-06-15' ) is None


def Test_FetchScheduleConflicts_TestOverlappingSchedule_ExpectConflictRecord(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   conflicts = GuardiansTalkScheduleProvider.fetch_schedule_conflicts(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-06-15',
         end_date='2026-07-15' ) )

   assert len( conflicts ) == 1
   assert conflicts[ 0 ].name == TALK_NAME
   assert conflicts[ 0 ].schedule_start_date == START_DATE
   assert conflicts[ 0 ].talk_time == TALK_TIME


def Test_FetchScheduleConflicts_TestNonOverlappingSchedule_ExpectEmpty(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   conflicts = GuardiansTalkScheduleProvider.fetch_schedule_conflicts(
      schedule_provider_conn,
      _schedule_input(
         start_date='2026-07-01',
         end_date='2026-07-31' ) )

   assert conflicts == []


def Test_DeleteSchedule_TestExistingSchedule_ExpectRemovesRow(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   GuardiansTalkScheduleProvider.delete_schedule(
      schedule_provider_conn,
      _schedule_record() )
   schedule_provider_conn.commit()

   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE ) is None


def Test_UpdateScheduleDates_TestExistingSchedule_ExpectUpdatesDates(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   GuardiansTalkScheduleProvider.update_schedule_dates(
      schedule_provider_conn,
      _schedule_record(),
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
   _insert_schedule_row( schedule_provider_conn )
   schedule_provider_conn.commit()

   GuardiansTalkScheduleProvider.insert_copied_schedule(
      schedule_provider_conn,
      _schedule_record(),
      '2026-08-01',
      '2026-08-31' )
   schedule_provider_conn.commit()

   row = _fetch_schedule_row(
      schedule_provider_conn,
      start_date='2026-08-01' )

   assert tuple( row ) == (
      TALK_NAME,
      LOCATION,
      '2026-08-01',
      '2026-08-31',
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      TALK_TIME,
      MESSAGE,
   )
   assert _fetch_schedule_row(
      schedule_provider_conn,
      start_date=START_DATE ) is not None


def Test_InsertOrUpdateSchedule_TestSameStartDate_ExpectUpdatesRow(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   GuardiansTalkScheduleProvider.insert_or_update_schedule(
      schedule_provider_conn,
      _schedule_input() )
   schedule_provider_conn.commit()

   GuardiansTalkScheduleProvider.insert_or_update_schedule(
      schedule_provider_conn,
      _schedule_input(
         end_date='2026-07-15',
         saturday=True,
         sunday=True,
         message='Updated talk hours.' ) )
   schedule_provider_conn.commit()

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert tuple( row ) == (
      TALK_NAME,
      LOCATION,
      START_DATE,
      '2026-07-15',
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      TALK_TIME,
      'Updated talk hours.',
   )


def Test_SaveScheduleEnd_TestCoveringSchedule_ExpectUpdatesEndDate(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule_row(
      schedule_provider_conn,
      end_date=None )
   schedule_provider_conn.commit()

   assert GuardiansTalkScheduleProvider.save_schedule_end(
      schedule_provider_conn,
      GuardiansTalkScheduleEndInput(
         talk_name=TALK_NAME,
         location=LOCATION,
         schedule_end_date='2026-06-20',
         talk_time=TALK_TIME ) ) is True

   row = _fetch_schedule_row( schedule_provider_conn, start_date=START_DATE )

   assert row is not None
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-06-20'


def Test_SaveScheduleEnd_TestNoMatchingSchedule_ExpectReturnsFalse(
      schedule_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkScheduleProvider.save_schedule_end(
      schedule_provider_conn,
      GuardiansTalkScheduleEndInput(
         talk_name=TALK_NAME,
         location=LOCATION,
         schedule_end_date='2026-06-20',
         talk_time=TALK_TIME ) ) is False
