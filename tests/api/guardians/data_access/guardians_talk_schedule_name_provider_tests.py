from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.guardians_talk_schedule_name_provider import GuardiansTalkScheduleNameProvider


TODAY = '2026-09-16'
LION = 'African Lion'
TIGER = 'Amur Tiger'
AFRICA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'

GUARDIANS_TALK_SCHEDULE_SCHEMA = """
CREATE TABLE GuardiansTalkSchedule (
   TALK_NAME           TEXT NOT NULL,
   LOCATION            TEXT NOT NULL,
   SCHEDULE_START_DATE TEXT NOT NULL,
   SCHEDULE_END_DATE   TEXT,
   TALK_TIME           TEXT NOT NULL,
   PRIMARY KEY ( TALK_NAME, LOCATION, TALK_TIME, SCHEDULE_START_DATE )
);
"""


@pytest.fixture
def guardians_talk_schedule_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( GUARDIANS_TALK_SCHEDULE_SCHEMA )

   yield conn

   conn.close()


def _insert_schedule(
      conn: sqlite3.Connection,
      *,
      talk_name: str,
      location: str,
      start_date: str,
      end_date: str | None,
      talk_time: str = '11:00 AM' ) -> None:
   conn.execute(
      """   INSERT INTO GuardiansTalkSchedule (
               TALK_NAME,
               LOCATION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               TALK_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         talk_name,
         location,
         start_date,
         end_date,
         talk_time,
      ) )
   conn.commit()


def Test_FetchScheduledTalkNames_TestEmpty_ExpectEmptyList(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_names(
      guardians_talk_schedule_name_conn,
      TODAY,
      AFRICA ) == []


def Test_FetchScheduledTalkNames_TestCurrentAndFuture_ExpectDistinctSortedTalks(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-09-01',
      end_date='2026-09-30',
      talk_time='2:00 PM' )
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=TIGER,
      location=AFRICA,
      start_date='2026-10-01',
      end_date='2026-10-15' )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_names(
      guardians_talk_schedule_name_conn,
      TODAY,
      AFRICA ) == [ LION, TIGER ]


def Test_FetchScheduledTalkNames_TestExpired_ExpectExcluded(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_names(
      guardians_talk_schedule_name_conn,
      TODAY,
      AFRICA ) == []


def Test_FetchScheduledTalkNames_TestEndingToday_ExpectExcluded(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_names(
      guardians_talk_schedule_name_conn,
      TODAY,
      AFRICA ) == []


def Test_FetchScheduledTalkNames_TestOtherLocation_ExpectExcluded(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=TIGER,
      location=EURASIA,
      start_date='2026-09-01',
      end_date='2026-09-30' )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_names(
      guardians_talk_schedule_name_conn,
      TODAY,
      AFRICA ) == []


def Test_FetchScheduledTalkLocations_TestEmpty_ExpectEmptyList(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_locations(
      guardians_talk_schedule_name_conn,
      TODAY ) == []


def Test_FetchScheduledTalkLocations_TestCurrentAndFuture_ExpectDistinctSortedLocations(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=TIGER,
      location=EURASIA,
      start_date='2026-10-01',
      end_date=None )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_locations(
      guardians_talk_schedule_name_conn,
      TODAY ) == [ AFRICA, EURASIA ]


def Test_FetchScheduledTalkLocations_TestExpired_ExpectExcluded(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_locations(
      guardians_talk_schedule_name_conn,
      TODAY ) == []


def Test_FetchScheduledTalkLocations_TestEndingToday_ExpectExcluded(
      guardians_talk_schedule_name_conn: sqlite3.Connection ) -> None:
   _insert_schedule(
      guardians_talk_schedule_name_conn,
      talk_name=LION,
      location=AFRICA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert GuardiansTalkScheduleNameProvider.fetch_scheduled_talk_locations(
      guardians_talk_schedule_name_conn,
      TODAY ) == []
