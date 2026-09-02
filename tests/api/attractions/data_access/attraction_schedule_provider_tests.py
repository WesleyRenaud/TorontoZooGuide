from __future__ import annotations

import sqlite3

import pytest

from api.attractions.data_access.attraction_schedule_provider import AttractionScheduleProvider
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.attractions.scheduling.attraction_opening_schedule import AttractionOpeningSchedule
from api.attractions.scheduling.attraction_schedule_override import AttractionScheduleOverride


ATTRACTION = 'Kids Zoo'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Summer hours.'
OVERRIDE_START = '2026-06-10'
OVERRIDE_END = '2026-06-12'
OVERRIDE_MESSAGE = 'Closed for private event.'

ATTRACTION_SCHEDULE_SCHEMA = """
CREATE TABLE AttractionOpeningSchedule (
   ATTRACTION            TEXT NOT NULL,
   SCHEDULE_START_DATE   TEXT NOT NULL,
   SCHEDULE_END_DATE     TEXT,
   MONDAY                INTEGER NOT NULL DEFAULT 0,
   TUESDAY               INTEGER NOT NULL DEFAULT 0,
   WEDNESDAY             INTEGER NOT NULL DEFAULT 0,
   THURSDAY              INTEGER NOT NULL DEFAULT 0,
   FRIDAY                INTEGER NOT NULL DEFAULT 0,
   SATURDAY              INTEGER NOT NULL DEFAULT 0,
   SUNDAY                INTEGER NOT NULL DEFAULT 0,
   HOLIDAYS_ONLY         INTEGER NOT NULL DEFAULT 0,
   SCHEDULE_MESSAGE      TEXT,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);

CREATE TABLE AttractionScheduleOverride (
   ATTRACTION            TEXT NOT NULL,
   OVERRIDE_START_DATE   TEXT NOT NULL,
   OVERRIDE_END_DATE     TEXT,
   IS_CLOSED             INTEGER NOT NULL DEFAULT 1,
   OVERRIDE_MESSAGE      TEXT,
   PRIMARY KEY ( ATTRACTION, OVERRIDE_START_DATE )
);
"""


def _opening_schedule(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE,
      monday: bool = True,
      tuesday: bool = True,
      wednesday: bool = True,
      thursday: bool = True,
      friday: bool = True,
      saturday: bool = False,
      sunday: bool = False,
      holidays_only: bool = False,
      message: str | None = MESSAGE ) -> AttractionOpeningSchedule:
   return AttractionOpeningSchedule(
      attraction=ATTRACTION,
      start_date=start_date,
      end_date=end_date,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      holidays_only=holidays_only,
      message=message )


def _schedule_record(
      *,
      start_date: str = START_DATE,
      end_date: str | None = END_DATE ) -> AttractionScheduleRecord:
   return AttractionScheduleRecord(
      attraction=ATTRACTION,
      schedule_start_date=start_date,
      schedule_end_date=end_date,
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=False,
      sunday=False,
      holidays_only=False,
      schedule_message=MESSAGE )


def _fetch_opening_row(
      conn: sqlite3.Connection,
      start_date: str ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               HOLIDAYS_ONLY,
               SCHEDULE_MESSAGE
            FROM AttractionOpeningSchedule
            WHERE ATTRACTION = ?
               AND SCHEDULE_START_DATE = ?;
      """,
      ( ATTRACTION, start_date ) ).fetchone()


@pytest.fixture
def attraction_schedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def Test_SaveOpeningSchedule_TestNewSchedule_ExpectPersistsRow(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   assert AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() ) is True

   row = _fetch_opening_row( attraction_schedule_conn, START_DATE )

   assert tuple( row ) == (
      ATTRACTION,
      START_DATE,
      END_DATE,
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      MESSAGE,
   )


def Test_SaveOpeningSchedule_TestSameStartDate_ExpectUpdatesRow(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   assert AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule(
         end_date='2026-07-15',
         saturday=True,
         sunday=True,
         message='Updated summer hours.' ) ) is True

   row = _fetch_opening_row( attraction_schedule_conn, START_DATE )

   assert tuple( row ) == (
      ATTRACTION,
      START_DATE,
      '2026-07-15',
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      0,
      'Updated summer hours.',
   )


def Test_SaveOpeningSchedule_TestOverlappingDates_ExpectReturnsFalse(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   assert AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Overlapping.' ) ) is False

   assert _fetch_opening_row( attraction_schedule_conn, '2026-06-15' ) is None


def Test_FetchOpeningScheduleConflicts_TestOverlappingSchedule_ExpectConflictRecord(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   conflicts = AttractionScheduleProvider.fetch_opening_schedule_conflicts(
      attraction_schedule_conn,
      _opening_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15' ) )

   assert len( conflicts ) == 1
   assert conflicts[ 0 ].attraction == ATTRACTION
   assert conflicts[ 0 ].schedule_start_date == START_DATE
   assert conflicts[ 0 ].schedule_end_date == END_DATE
   assert conflicts[ 0 ].schedule_message == MESSAGE


def Test_FetchOpeningScheduleConflicts_TestNonOverlappingSchedule_ExpectEmpty(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   conflicts = AttractionScheduleProvider.fetch_opening_schedule_conflicts(
      attraction_schedule_conn,
      _opening_schedule(
         start_date='2026-07-01',
         end_date='2026-07-31' ) )

   assert conflicts == []


def Test_DeleteOpeningSchedule_TestExistingSchedule_ExpectRemovesRow(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   AttractionScheduleProvider.delete_opening_schedule(
      attraction_schedule_conn,
      _schedule_record() )

   assert _fetch_opening_row( attraction_schedule_conn, START_DATE ) is None


def Test_UpdateOpeningScheduleDates_TestExistingSchedule_ExpectUpdatesDates(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   AttractionScheduleProvider.update_opening_schedule_dates(
      attraction_schedule_conn,
      _schedule_record(),
      '2026-07-01',
      '2026-07-31' )

   assert _fetch_opening_row( attraction_schedule_conn, START_DATE ) is None

   row = _fetch_opening_row( attraction_schedule_conn, '2026-07-01' )

   assert row is not None
   assert row[ 'SCHEDULE_START_DATE' ] == '2026-07-01'
   assert row[ 'SCHEDULE_END_DATE' ] == '2026-07-31'
   assert row[ 'SCHEDULE_MESSAGE' ] == MESSAGE


def Test_InsertCopiedOpeningSchedule_TestExistingSchedule_ExpectInsertsCopy(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_opening_schedule(
      attraction_schedule_conn,
      _opening_schedule() )

   AttractionScheduleProvider.insert_copied_opening_schedule(
      attraction_schedule_conn,
      _schedule_record(),
      '2026-08-01',
      '2026-08-31' )

   row = _fetch_opening_row( attraction_schedule_conn, '2026-08-01' )

   assert tuple( row ) == (
      ATTRACTION,
      '2026-08-01',
      '2026-08-31',
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      MESSAGE,
   )
   assert _fetch_opening_row( attraction_schedule_conn, START_DATE ) is not None


def Test_SaveScheduleOverride_TestNewOverride_ExpectPersistsRow(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   override = AttractionScheduleOverride(
      attraction=ATTRACTION,
      start_date=OVERRIDE_START,
      end_date=OVERRIDE_END,
      is_closed=True,
      message=OVERRIDE_MESSAGE )

   assert AttractionScheduleProvider.save_schedule_override(
      attraction_schedule_conn,
      override ) is True

   row = attraction_schedule_conn.execute(
      """   SELECT
               ATTRACTION,
               OVERRIDE_START_DATE,
               OVERRIDE_END_DATE,
               IS_CLOSED,
               OVERRIDE_MESSAGE
            FROM AttractionScheduleOverride
            WHERE ATTRACTION = ?
               AND OVERRIDE_START_DATE = ?;
      """,
      ( ATTRACTION, OVERRIDE_START ) ).fetchone()

   assert tuple( row ) == (
      ATTRACTION,
      OVERRIDE_START,
      OVERRIDE_END,
      1,
      OVERRIDE_MESSAGE,
   )


def Test_SaveScheduleOverride_TestExistingOverride_ExpectUpdatesRow(
      attraction_schedule_conn: sqlite3.Connection ) -> None:
   AttractionScheduleProvider.save_schedule_override(
      attraction_schedule_conn,
      AttractionScheduleOverride(
         attraction=ATTRACTION,
         start_date=OVERRIDE_START,
         end_date=OVERRIDE_END,
         is_closed=True,
         message=OVERRIDE_MESSAGE ) )

   assert AttractionScheduleProvider.save_schedule_override(
      attraction_schedule_conn,
      AttractionScheduleOverride(
         attraction=ATTRACTION,
         start_date=OVERRIDE_START,
         end_date='2026-06-14',
         is_closed=False,
         message='Special open day.' ) ) is True

   row = attraction_schedule_conn.execute(
      """   SELECT OVERRIDE_END_DATE, IS_CLOSED, OVERRIDE_MESSAGE
            FROM AttractionScheduleOverride
            WHERE ATTRACTION = ?
               AND OVERRIDE_START_DATE = ?;
      """,
      ( ATTRACTION, OVERRIDE_START ) ).fetchone()

   assert tuple( row ) == ( '2026-06-14', 0, 'Special open day.' )
