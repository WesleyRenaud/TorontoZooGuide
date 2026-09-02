from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from api.guardians.occurrences.guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput


TALK_NAME = 'African Lion'
LOCATION = 'Africa Savanna'
X_COORD = 1.5
Y_COORD = 2.5
MAXIMUM_DURATION = 20
TALK_TIME = '11:00 AM'
SECOND_TALK_TIME = '2:00 PM'
OCCURRENCE_DATE = '2026-06-15'  # Monday
WEEKEND_DATE = '2026-06-13'  # Saturday
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'

OCCURRENCE_PROVIDER_SCHEMA = """
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

CREATE TABLE GuardiansTalkOccurrence (
   TALK_NAME        TEXT NOT NULL,
   LOCATION         TEXT NOT NULL,
   OCCURRENCE_DATE  DATE NOT NULL,
   TALK_TIME        TEXT NOT NULL,
   PRIMARY KEY ( TALK_NAME, LOCATION, OCCURRENCE_DATE, TALK_TIME )
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
def occurrence_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( OCCURRENCE_PROVIDER_SCHEMA )
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


def _occurrence_input(
      *,
      occurrence_date: str = OCCURRENCE_DATE,
      talk_time: str = TALK_TIME ) -> GuardiansTalkOccurrenceInput:
   return GuardiansTalkOccurrenceInput(
      talk_name=TALK_NAME,
      location=LOCATION,
      occurrence_date=occurrence_date,
      talk_time=talk_time )


def _insert_occurrence(
      conn: sqlite3.Connection,
      *,
      occurrence_date: str = OCCURRENCE_DATE,
      talk_time: str = TALK_TIME ) -> None:
   conn.execute(
      """   INSERT INTO GuardiansTalkOccurrence (
               TALK_NAME, LOCATION, OCCURRENCE_DATE, TALK_TIME
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( TALK_NAME, LOCATION, occurrence_date, talk_time ),
   )


def _insert_schedule(
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
      sunday: int = 0 ) -> None:
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
         None,
      ),
   )


def Test_OccurrenceRecordExists_TestMissing_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.occurrence_record_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is False


def Test_OccurrenceRecordExists_TestPersisted_ExpectTrue(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_occurrence( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.occurrence_record_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is True


def Test_OccurrenceExists_TestExplicitRecord_ExpectTrue(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_occurrence( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is True


def Test_OccurrenceExists_TestNoneDate_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      None,  # type: ignore[arg-type]
      TALK_TIME ) is False


def Test_OccurrenceExists_TestScheduleOutsideDateRange_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      '2026-07-15',
      TALK_TIME ) is False


def Test_OccurrenceExists_TestScheduleCoversWeekday_ExpectTrue(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is True


def Test_OccurrenceExists_TestScheduleExcludesWeekday_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_schedule( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      WEEKEND_DATE,
      TALK_TIME ) is False


def Test_OccurrenceExists_TestNoMatchingSchedule_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.occurrence_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is False


def Test_SaveOccurrence_TestNewRow_ExpectTrueAndPersisted(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.save_occurrence(
      occurrence_provider_conn,
      _occurrence_input() ) is True

   assert GuardiansTalkOccurrenceProvider.occurrence_record_exists(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      OCCURRENCE_DATE,
      TALK_TIME ) is True


def Test_SaveOccurrence_TestDuplicate_ExpectFalse(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   GuardiansTalkOccurrenceProvider.save_occurrence(
      occurrence_provider_conn,
      _occurrence_input() )

   assert GuardiansTalkOccurrenceProvider.save_occurrence(
      occurrence_provider_conn,
      _occurrence_input() ) is False


def Test_FetchOccurrenceRecords_TestEmptyRange_ExpectEmptyList(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.fetch_occurrence_records(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      start_date=START_DATE,
      end_date=END_DATE ) == []


def Test_FetchOccurrenceRecords_TestDateRange_ExpectOrderedMatchingRows(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_occurrence(
      occurrence_provider_conn,
      occurrence_date='2026-06-10',
      talk_time=SECOND_TALK_TIME )
   _insert_occurrence(
      occurrence_provider_conn,
      occurrence_date='2026-06-10',
      talk_time=TALK_TIME )
   _insert_occurrence(
      occurrence_provider_conn,
      occurrence_date='2026-06-20',
      talk_time=TALK_TIME )
   _insert_occurrence(
      occurrence_provider_conn,
      occurrence_date='2026-07-01',
      talk_time=TALK_TIME )
   occurrence_provider_conn.commit()

   records = GuardiansTalkOccurrenceProvider.fetch_occurrence_records(
      occurrence_provider_conn,
      TALK_NAME,
      LOCATION,
      start_date='2026-06-10',
      end_date='2026-06-20' )

   assert [
      ( record.occurrence_date, record.talk_time )
      for record in records
   ] == [
      ( '2026-06-10', TALK_TIME ),
      ( '2026-06-10', SECOND_TALK_TIME ),
      ( '2026-06-20', TALK_TIME ),
   ]


def Test_FetchDayScheduleRecordsFromOccurrences_TestEmpty_ExpectEmptyList(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkOccurrenceProvider.fetch_day_schedule_records_from_occurrences(
      occurrence_provider_conn,
      OCCURRENCE_DATE ) == []


def Test_FetchDayScheduleRecordsFromOccurrences_TestActiveOccurrence_ExpectMappedTalk(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_occurrence( occurrence_provider_conn )
   occurrence_provider_conn.commit()

   records = GuardiansTalkOccurrenceProvider.fetch_day_schedule_records_from_occurrences(
      occurrence_provider_conn,
      OCCURRENCE_DATE )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == TALK_NAME
   assert record.location == LOCATION
   assert record.x_coord == X_COORD
   assert record.y_coord == Y_COORD
   assert record.maximum_duration == MAXIMUM_DURATION
   assert record.talk_time == TALK_TIME


def Test_FetchDayScheduleRecordsFromOccurrences_TestCancelled_ExpectExcluded(
      occurrence_provider_conn: sqlite3.Connection ) -> None:
   _insert_occurrence( occurrence_provider_conn )
   occurrence_provider_conn.execute(
      """   INSERT INTO GuardiansTalkCancellation (
               TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( TALK_NAME, LOCATION, OCCURRENCE_DATE, TALK_TIME ),
   )
   occurrence_provider_conn.commit()

   assert GuardiansTalkOccurrenceProvider.fetch_day_schedule_records_from_occurrences(
      occurrence_provider_conn,
      OCCURRENCE_DATE ) == []
