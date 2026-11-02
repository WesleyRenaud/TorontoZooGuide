from __future__ import annotations

import sqlite3

import pytest

from api.attractions.data_access.attraction_status_provider import AttractionStatusProvider
from api.shared.enums.position import Position


ATTRACTION = 'Conservation Carousel'
OTHER_ATTRACTION = 'Zoomobile'
CLOSED_MESSAGE = 'The Conservation Carousel is closed for the season.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
TODAY = '2026-11-02'

ATTRACTION_STATUS_SCHEMA = """
CREATE TABLE AttractionStatus (
   ATTRACTION          TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED           INTEGER NOT NULL,
   CLOSED_MESSAGE      TEXT,
   CLOSED_START        TEXT,
   CLOSED_END          TEXT,
   CLOSED_FOR_SEASON   INTEGER NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def attraction_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_STATUS_SCHEMA )

   yield conn

   conn.close()


def _fetch_status_row( conn: sqlite3.Connection, attraction: str = ATTRACTION ) -> sqlite3.Row:
   return conn.execute(
      """   SELECT
               ATTRACTION,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM AttractionStatus
            WHERE ATTRACTION = ?;
      """,
      ( attraction, ) ).fetchone()


def Test_SaveClosedForSeason_TestNewAttraction_ExpectPersistsSeasonRow(
      attraction_status_conn: sqlite3.Connection ) -> None:
   result = AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   assert result is True
   assert tuple( _fetch_status_row( attraction_status_conn ) ) == (
      ATTRACTION, 1, CLOSED_MESSAGE, START_DATE, END_DATE, 1 )


def Test_SaveClosedForSeason_TestExistingRow_ExpectReplacesWindow(
      attraction_status_conn: sqlite3.Connection ) -> None:
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date='2026-10-01',
      end_date=None,
      message='Closed until spring.' )

   row = _fetch_status_row( attraction_status_conn )

   assert row[ 'CLOSED_START' ] == '2026-10-01'
   assert row[ 'CLOSED_END' ] is None
   assert row[ 'CLOSED_MESSAGE' ] == 'Closed until spring.'
   assert row[ 'CLOSED_FOR_SEASON' ] == 1


def Test_DeleteClosedForSeason_TestExistingRow_ExpectRemoved(
      attraction_status_conn: sqlite3.Connection ) -> None:
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   result = AttractionStatusProvider.delete_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION )

   assert result is True
   assert _fetch_status_row( attraction_status_conn ) is None


def Test_DeleteClosedForSeason_TestMissingRow_ExpectFalse(
      attraction_status_conn: sqlite3.Connection ) -> None:
   result = AttractionStatusProvider.delete_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION )

   assert result is False


def Test_FetchClosedForSeasonNames_TestExpiredAndCurrent_ExpectCurrentOnly(
      attraction_status_conn: sqlite3.Connection ) -> None:
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=OTHER_ATTRACTION,
      start_date=START_DATE,
      end_date='2026-10-01',
      message=CLOSED_MESSAGE )

   names = AttractionStatusProvider.fetch_closed_for_season_names(
      attraction_status_conn,
      today=TODAY )

   assert names == [ ATTRACTION ]


def Test_FetchClosureRecord_TestSavedRow_ExpectMappedRecord(
      attraction_status_conn: sqlite3.Connection ) -> None:
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   record = AttractionStatusProvider.fetch_closure_record(
      attraction_status_conn,
      attraction=ATTRACTION )

   assert record is not None
   assert record.attraction == ATTRACTION
   assert record.closed_start == START_DATE
   assert record.closed_end is None
   assert record.closed_message == CLOSED_MESSAGE
   assert record.is_closed_for_season is True


def Test_FetchClosureRecord_TestMissingAttraction_ExpectNone(
      attraction_status_conn: sqlite3.Connection ) -> None:
   record = AttractionStatusProvider.fetch_closure_record(
      attraction_status_conn,
      attraction=ATTRACTION )

   assert record == None


def Test_FetchClosureRecords_TestSavedRows_ExpectAllSeasonClosures(
      attraction_status_conn: sqlite3.Connection ) -> None:
   AttractionStatusProvider.save_closed_for_season(
      attraction_status_conn,
      attraction=ATTRACTION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   records = AttractionStatusProvider.fetch_closure_records( attraction_status_conn )

   assert len( records ) == 1
   assert records[ Position.FIRST ].attraction == ATTRACTION
