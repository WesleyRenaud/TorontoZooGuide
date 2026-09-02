from __future__ import annotations

import sqlite3

import pytest

from api.guardians.cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from api.guardians.data_access.guardians_talk_cancellation_provider import GuardiansTalkCancellationProvider


TALK_NAME = 'African Lion'
LOCATION = 'Africa Savanna'
TALK_TIME = '11:00 AM'
SECOND_TALK_TIME = '2:00 PM'
CANCELLATION_DATE = '2026-06-15'
OTHER_DATE = '2026-06-20'

CANCELLATION_PROVIDER_SCHEMA = """
CREATE TABLE GuardiansTalkCancellation (
   TALK_NAME         TEXT NOT NULL,
   LOCATION          TEXT NOT NULL,
   CANCELLATION_DATE DATE NOT NULL,
   TALK_TIME         TEXT NOT NULL,
   PRIMARY KEY ( TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME )
);
"""


@pytest.fixture
def cancellation_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( CANCELLATION_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _cancellation_input(
      *,
      cancellation_date: str = CANCELLATION_DATE,
      talk_time: str = TALK_TIME ) -> GuardiansTalkCancellationInput:
   return GuardiansTalkCancellationInput(
      talk_name=TALK_NAME,
      location=LOCATION,
      cancellation_date=cancellation_date,
      talk_time=talk_time )


def _insert_cancellation(
      conn: sqlite3.Connection,
      *,
      cancellation_date: str = CANCELLATION_DATE,
      talk_time: str = TALK_TIME,
      talk_name: str = TALK_NAME,
      location: str = LOCATION ) -> None:
   conn.execute(
      """   INSERT INTO GuardiansTalkCancellation (
               TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( talk_name, location, cancellation_date, talk_time ),
   )


def Test_FetchCancellationRecords_TestEmpty_ExpectEmptyList(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkCancellationProvider.fetch_cancellation_records(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION ) == []


def Test_FetchCancellationRecords_TestMatchingTalk_ExpectMappedRecords(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   _insert_cancellation( cancellation_provider_conn )
   _insert_cancellation(
      cancellation_provider_conn,
      cancellation_date=OTHER_DATE,
      talk_time=SECOND_TALK_TIME )
   _insert_cancellation(
      cancellation_provider_conn,
      talk_name='Other Talk',
      location=LOCATION )
   cancellation_provider_conn.commit()

   records = GuardiansTalkCancellationProvider.fetch_cancellation_records(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION )

   assert [
      ( record.cancellation_date, record.talk_time )
      for record in records
   ] == [
      ( CANCELLATION_DATE, TALK_TIME ),
      ( OTHER_DATE, SECOND_TALK_TIME ),
   ]


def Test_FetchOccurrenceIsCancelled_TestMissing_ExpectFalse(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkCancellationProvider.fetch_occurrence_is_cancelled(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION,
      CANCELLATION_DATE,
      TALK_TIME ) is False


def Test_FetchOccurrenceIsCancelled_TestMatching_ExpectTrue(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   _insert_cancellation( cancellation_provider_conn )
   cancellation_provider_conn.commit()

   assert GuardiansTalkCancellationProvider.fetch_occurrence_is_cancelled(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION,
      CANCELLATION_DATE,
      TALK_TIME ) is True


def Test_FetchOccurrenceIsCancelled_TestDifferentTime_ExpectFalse(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   _insert_cancellation( cancellation_provider_conn )
   cancellation_provider_conn.commit()

   assert GuardiansTalkCancellationProvider.fetch_occurrence_is_cancelled(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION,
      CANCELLATION_DATE,
      SECOND_TALK_TIME ) is False


def Test_SaveCancellation_TestNewRow_ExpectTrueAndPersisted(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   assert GuardiansTalkCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() ) is True

   assert GuardiansTalkCancellationProvider.fetch_occurrence_is_cancelled(
      cancellation_provider_conn,
      TALK_NAME,
      LOCATION,
      CANCELLATION_DATE,
      TALK_TIME ) is True


def Test_SaveCancellation_TestDuplicate_ExpectFalse(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   GuardiansTalkCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() )

   assert GuardiansTalkCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() ) is False
