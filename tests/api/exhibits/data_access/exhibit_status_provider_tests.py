from __future__ import annotations

import sqlite3

import pytest

from api.exhibits.data_access.exhibit_status_provider import ExhibitStatusProvider


EXHIBIT = 'Africa Savanna'
CLOSED_MESSAGE = 'Closed for maintenance.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'

EXHIBIT_STATUS_SCHEMA = """
CREATE TABLE ExhibitStatus (
   EXHIBIT          TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED        INTEGER NOT NULL,
   CLOSED_MESSAGE   TEXT,
   CLOSED_START     TEXT,
   CLOSED_END       TEXT
);
"""


@pytest.fixture
def exhibit_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EXHIBIT_STATUS_SCHEMA )

   yield conn

   conn.close()


def Test_SaveClosedStatus_TestNewExhibit_ExpectPersistsClosedRow(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   assert ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE ) is True

   row = exhibit_status_conn.execute(
      """   SELECT EXHIBIT, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            FROM ExhibitStatus
            WHERE EXHIBIT = ?;
      """,
      ( EXHIBIT, ) ).fetchone()

   assert tuple( row ) == ( EXHIBIT, 1, CLOSED_MESSAGE, START_DATE, END_DATE )


def Test_SaveOpenStatus_TestPreviouslyClosedExhibit_ExpectClearsClosedMessage(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   assert ExhibitStatusProvider.save_open_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE ) is True

   row = exhibit_status_conn.execute(
      """   SELECT IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            FROM ExhibitStatus
            WHERE EXHIBIT = ?;
      """,
      ( EXHIBIT, ) ).fetchone()

   assert tuple( row ) == ( 0, None, START_DATE, END_DATE )


def Test_FetchClosureRecords_TestMixedStatuses_ExpectOnlyClosedExhibits(
      exhibit_status_conn: sqlite3.Connection ) -> None:
   ExhibitStatusProvider.save_closed_status(
      exhibit_status_conn,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )
   ExhibitStatusProvider.save_open_status(
      exhibit_status_conn,
      exhibit='Indo-Malaya',
      start_date=START_DATE,
      end_date=END_DATE )

   records = ExhibitStatusProvider.fetch_closure_records( exhibit_status_conn )

   assert len( records ) == 1
   assert records[ 0 ].exhibit == EXHIBIT
   assert records[ 0 ].closed_start == START_DATE
   assert records[ 0 ].closed_end == END_DATE
