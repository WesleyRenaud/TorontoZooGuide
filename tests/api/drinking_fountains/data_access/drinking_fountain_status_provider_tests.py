from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.drinking_fountains.data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from api.drinking_fountains.status.drinking_fountain_closed_status import DrinkingFountainClosedStatus
from api.drinking_fountains.status.drinking_fountain_open_status import DrinkingFountainOpenStatus


START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
CLOSED_MESSAGE = 'Seasonal shutdown.'

DRINKING_FOUNTAIN_STATUS_SCHEMA = """
CREATE TABLE DrinkingFountainStatus (
   IS_CLOSED        INTEGER NOT NULL,
   START_DATE       TEXT,
   END_DATE         TEXT,
   CLOSED_MESSAGE   TEXT
);

CREATE TABLE DrinkingFountainDaySeasonalAvailabilityMultiplier (
   MONTH            INTEGER NOT NULL,
   DAY              INTEGER NOT NULL,
   LIKELIHOOD       REAL NOT NULL,
   PRIMARY KEY ( MONTH, DAY )
);
"""


@pytest.fixture
def drinking_fountain_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DRINKING_FOUNTAIN_STATUS_SCHEMA )
   conn.execute(
      """   INSERT INTO DrinkingFountainDaySeasonalAvailabilityMultiplier (
               MONTH,
               DAY,
               LIKELIHOOD
            )
            VALUES ( 6, 15, 0.5 );
      """ )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchDrinkingFountainStatusRecord_TestEmptyTable_ExpectNone(
      drinking_fountain_status_conn: sqlite3.Connection ) -> None:
   assert DrinkingFountainStatusProvider.fetch_drinking_fountain_status_record(
      drinking_fountain_status_conn ) is None


def Test_SaveClosedStatus_TestClosedStatus_ExpectPersistsAndFetches(
      drinking_fountain_status_conn: sqlite3.Connection ) -> None:
   assert DrinkingFountainStatusProvider.save_drinking_fountain_closed_status(
      drinking_fountain_status_conn,
      DrinkingFountainClosedStatus(
         start_date=START_DATE,
         end_date=END_DATE,
         message=CLOSED_MESSAGE ) ) is True

   record = DrinkingFountainStatusProvider.fetch_drinking_fountain_status_record(
      drinking_fountain_status_conn )

   assert record is not None
   assert record.is_closed == 1
   assert record.start_date == START_DATE
   assert record.end_date == END_DATE
   assert record.closed_message == CLOSED_MESSAGE


def Test_SaveOpenStatus_TestReplacesClosedStatus_ExpectOpenRow(
      drinking_fountain_status_conn: sqlite3.Connection ) -> None:
   DrinkingFountainStatusProvider.save_drinking_fountain_closed_status(
      drinking_fountain_status_conn,
      DrinkingFountainClosedStatus(
         start_date=START_DATE,
         end_date=END_DATE,
         message=CLOSED_MESSAGE ) )

   assert DrinkingFountainStatusProvider.save_drinking_fountain_open_status(
      drinking_fountain_status_conn,
      DrinkingFountainOpenStatus(
         start_date=START_DATE,
         end_date=END_DATE ) ) is True

   record = DrinkingFountainStatusProvider.fetch_drinking_fountain_status_record(
      drinking_fountain_status_conn )

   assert record is not None
   assert record.is_closed == 0
   assert record.closed_message is None


def Test_FetchSeasonalLikelihood_TestKnownDate_ExpectStoredLikelihood(
      drinking_fountain_status_conn: sqlite3.Connection ) -> None:
   assert DrinkingFountainStatusProvider.fetch_drinking_fountain_seasonal_likelihood(
      drinking_fountain_status_conn,
      date( 2026, 6, 15 ) ) == 0.5


def Test_FetchSeasonalLikelihood_TestUnknownDate_ExpectDefaultOne(
      drinking_fountain_status_conn: sqlite3.Connection ) -> None:
   assert DrinkingFountainStatusProvider.fetch_drinking_fountain_seasonal_likelihood(
      drinking_fountain_status_conn,
      date( 2026, 1, 1 ) ) == 1.0
