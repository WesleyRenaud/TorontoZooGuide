from __future__ import annotations

import sqlite3

import pytest

from api.exhibits.data_access.exhibit_status_provider import ExhibitStatusProvider
from api.shared.enums.position import Position


EXHIBIT = 'Africa Savanna'
CLOSED_MESSAGE = 'Closed for maintenance.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'

EXHIBIT_STATUS_SCHEMA = """
CREATE TABLE ExhibitStatus (
   EXHIBIT             TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED           INTEGER NOT NULL,
   CLOSED_MESSAGE      TEXT,
   CLOSED_START        TEXT,
   CLOSED_END          TEXT,
   CLOSED_FOR_SEASON   INTEGER NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def exhibit_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EXHIBIT_STATUS_SCHEMA )

   yield conn

   conn.close()


def _fetch_status_row( conn: sqlite3.Connection ) -> sqlite3.Row:
   return conn.execute(
      """   SELECT EXHIBIT, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END, CLOSED_FOR_SEASON
            FROM ExhibitStatus
            WHERE EXHIBIT = ?;
      """,
      ( EXHIBIT, ) ).fetchone()


def Test_SaveClosedStatus_TestNewExhibit_ExpectPersistsClosedRow(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   result = ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=False )

   assert result is True
   assert tuple( _fetch_status_row( exhibit_status_conn ) ) == (
      EXHIBIT, 1, CLOSED_MESSAGE, START_DATE, END_DATE, 0 )


def Test_SaveClosedStatus_TestClosedForSeason_ExpectPersistsSeasonFlag(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   result = ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=True )

   assert result is True
   assert tuple( _fetch_status_row( exhibit_status_conn ) ) == (
      EXHIBIT, 1, CLOSED_MESSAGE, START_DATE, END_DATE, 1 )


def Test_SaveClosedStatus_TestExistingSeasonClosure_ExpectSeasonFlagReplaced(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=True )

   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=False )

   assert _fetch_status_row( exhibit_status_conn )[ 'CLOSED_FOR_SEASON' ] == 0


def Test_SaveOpenStatus_TestPreviouslyClosedExhibit_ExpectClearsClosedMessage(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=True )

   result = ExhibitStatusProvider.save_open_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE )

   assert result is True
   assert tuple( _fetch_status_row( exhibit_status_conn ) ) == (
      EXHIBIT, 0, None, START_DATE, END_DATE, 0 )


def Test_FetchClosureRecords_TestMixedStatuses_ExpectOnlyClosedExhibits(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE,
      is_closed_for_season=False )
   ExhibitStatusProvider.save_open_status(
      exhibit_status_conn,
      exhibit='Indo-Malaya',
      start_date=START_DATE,
      end_date=END_DATE )

   records = ExhibitStatusProvider.fetch_closure_records( exhibit_status_conn )

   assert len( records ) == 1
   assert records[ Position.FIRST ].exhibit == EXHIBIT
   assert records[ Position.FIRST ].closed_start == START_DATE
   assert records[ Position.FIRST ].closed_end == END_DATE
