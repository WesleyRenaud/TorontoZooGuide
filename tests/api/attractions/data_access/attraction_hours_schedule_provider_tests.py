from __future__ import annotations

import sqlite3

import pytest

from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.attractions.data_access.attraction_hours_schedule_record import AttractionHoursScheduleRecord
from api.attractions.scheduling.attraction_hours_schedule import AttractionHoursSchedule


ATTRACTION = 'Kids Zoo'
OTHER_ATTRACTION = 'Splash Island'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
WEEKDAY_START = '10:00'
WEEKDAY_END = '16:00'
WEEKEND_START = '09:00'
WEEKEND_END = '17:00'

ATTRACTION_HOURS_SCHEDULE_SCHEMA = """
CREATE TABLE AttractionHoursSchedule (
   ATTRACTION                      TEXT NOT NULL,
   SCHEDULE_START_DATE             TEXT NOT NULL,
   SCHEDULE_END_DATE               TEXT,
   WEEKDAY_START_TIME              TEXT NOT NULL,
   WEEKDAY_END_TIME                TEXT NOT NULL,
   WEEKEND_HOLIDAY_START_TIME      TEXT NOT NULL,
   WEEKEND_HOLIDAY_END_TIME        TEXT NOT NULL,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);
"""


def _hours_schedule(
      *,
      attraction: str = ATTRACTION,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      weekday_start_time: str = WEEKDAY_START,
      weekday_end_time: str = WEEKDAY_END,
      weekend_holiday_start_time: str = WEEKEND_START,
      weekend_holiday_end_time: str = WEEKEND_END ) -> AttractionHoursSchedule:
   return AttractionHoursSchedule(
      attraction=attraction,
      start_date=start_date,
      end_date=end_date,
      weekday_start_time=weekday_start_time,
      weekday_end_time=weekday_end_time,
      weekend_holiday_start_time=weekend_holiday_start_time,
      weekend_holiday_end_time=weekend_holiday_end_time )


def _hours_record(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE ) -> AttractionHoursScheduleRecord:
   return AttractionHoursScheduleRecord(
      attraction=ATTRACTION,
      schedule_start_date=start_date,
      schedule_end_date=end_date,
      weekday_start_time=WEEKDAY_START,
      weekday_end_time=WEEKDAY_END,
      weekend_holiday_start_time=WEEKEND_START,
      weekend_holiday_end_time=WEEKEND_END )


def _fetch_hours_row(
      conn: sqlite3.Connection,
      start_date: str,
      attraction: str = ATTRACTION ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            FROM AttractionHoursSchedule
            WHERE ATTRACTION = ?
               AND SCHEDULE_START_DATE = ?;
      """,
      ( attraction, start_date ) ).fetchone()


@pytest.fixture
def attraction_hours_schedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_HOURS_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def Test_SaveHoursSchedule_TestNewSchedule_ExpectPersistsRow(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   assert AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() ) is True

   row = _fetch_hours_row( attraction_hours_schedule_conn, START_DATE )

   assert tuple( row ) == (
      ATTRACTION,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END,
   )


def Test_SaveHoursSchedule_TestSameStartDate_ExpectUpdatesRow(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   assert AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule(
         end_date='2026-07-15',
         weekday_start_time='11:00',
         weekday_end_time='15:00',
         weekend_holiday_start_time='10:00',
         weekend_holiday_end_time='16:00' ) ) is True

   row = _fetch_hours_row( attraction_hours_schedule_conn, START_DATE )

   assert tuple( row ) == (
      ATTRACTION,
      START_DATE,
      '2026-07-15',
      '11:00',
      '15:00',
      '10:00',
      '16:00',
   )


def Test_SaveHoursSchedule_TestOverlappingDates_ExpectReturnsFalse(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   assert AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15' ) ) is False

   assert _fetch_hours_row( attraction_hours_schedule_conn, '2026-06-15' ) is None


def Test_FetchHoursScheduleConflicts_TestOverlappingSchedule_ExpectConflictRecord(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   conflicts = AttractionHoursScheduleProvider.fetch_hours_schedule_conflicts(
      attraction_hours_schedule_conn,
      _hours_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15' ) )

   assert len( conflicts ) == 1
   assert conflicts[ 0 ].attraction == ATTRACTION
   assert conflicts[ 0 ].schedule_start_date == START_DATE
   assert conflicts[ 0 ].schedule_end_date == END_DATE
   assert conflicts[ 0 ].weekday_start_time == WEEKDAY_START
   assert conflicts[ 0 ].weekend_holiday_end_time == WEEKEND_END


def Test_FetchHoursScheduleConflicts_TestNonOverlappingSchedule_ExpectEmpty(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   conflicts = AttractionHoursScheduleProvider.fetch_hours_schedule_conflicts(
      attraction_hours_schedule_conn,
      _hours_schedule(
         start_date='2026-07-01',
         end_date='2026-07-31' ) )

   assert conflicts == []


def Test_FetchHoursScheduleRecords_TestMultipleSchedules_ExpectOrderedRecords(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule(
         attraction=OTHER_ATTRACTION,
         start_date='2026-07-01',
         end_date='2026-07-31' ) )
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   records = AttractionHoursScheduleProvider.fetch_hours_schedule_records(
      attraction_hours_schedule_conn )

   assert len( records ) == 2
   assert records[ 0 ].attraction == ATTRACTION
   assert records[ 0 ].schedule_start_date == START_DATE
   assert records[ 1 ].attraction == OTHER_ATTRACTION
   assert records[ 1 ].schedule_start_date == '2026-07-01'


def Test_DeleteHoursSchedule_TestExistingSchedule_ExpectRemovesRow(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   AttractionHoursScheduleProvider.delete_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_record() )

   assert _fetch_hours_row( attraction_hours_schedule_conn, START_DATE ) is None


def Test_UpdateHoursScheduleDates_TestExistingSchedule_ExpectUpdatesDates(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   AttractionHoursScheduleProvider.update_hours_schedule_dates(
      attraction_hours_schedule_conn,
      _hours_record(),
      '2026-07-01',
      '2026-07-31' )

   assert _fetch_hours_row( attraction_hours_schedule_conn, START_DATE ) is None

   row = _fetch_hours_row( attraction_hours_schedule_conn, '2026-07-01' )

   assert row is not None
   assert row[ 'SCHEDULE_START_DATE' ] == '2026-07-01'
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-07-31'
   assert row[ 'WEEKDAY_START_TIME' ] == WEEKDAY_START


def Test_InsertCopiedHoursSchedule_TestExistingSchedule_ExpectInsertsCopy(
      attraction_hours_schedule_conn: sqlite3.Connection ) -> None:
   AttractionHoursScheduleProvider.save_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_schedule() )

   AttractionHoursScheduleProvider.insert_copied_hours_schedule(
      attraction_hours_schedule_conn,
      _hours_record(),
      '2026-08-01',
      '2026-08-31' )

   row = _fetch_hours_row( attraction_hours_schedule_conn, '2026-08-01' )

   assert tuple( row ) == (
      ATTRACTION,
      '2026-08-01',
      '2026-08-31',
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END,
   )
   assert _fetch_hours_row( attraction_hours_schedule_conn, START_DATE ) is not None
