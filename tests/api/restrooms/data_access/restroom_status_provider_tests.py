from __future__ import annotations

import sqlite3

import pytest

from api.restrooms.data_access.restroom_status_provider import RestroomStatusProvider


RESTROOM = 'Entrance Restroom'
CLOSED_MESSAGE = 'Out of order.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'

RESTROOM_STATUS_SCHEMA = """
CREATE TABLE RestroomStatus (
   RESTROOM         TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED        INTEGER NOT NULL,
   CLOSED_MESSAGE   TEXT,
   CLOSED_START     TEXT,
   CLOSED_END       TEXT
);
"""


@pytest.fixture
def restroom_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTROOM_STATUS_SCHEMA )

   yield conn

   conn.close()


def Test_SaveClosedStatus_TestNewRestroom_ExpectPersistsClosedRow(
      restroom_status_conn: sqlite3.Connection ) -> None:
   assert RestroomStatusProvider.save_closed_status(
      restroom_status_conn,
      restroom=RESTROOM,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE ) is True

   row = restroom_status_conn.execute(
      """   SELECT RESTROOM, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            FROM RestroomStatus
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchone()

   assert tuple( row ) == ( RESTROOM, 1, CLOSED_MESSAGE, START_DATE, END_DATE )


def Test_SaveOpenStatus_TestPreviouslyClosedRestroom_ExpectClearsClosedMessage(
      restroom_status_conn: sqlite3.Connection ) -> None:
   RestroomStatusProvider.save_closed_status(
      restroom_status_conn,
      restroom=RESTROOM,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   assert RestroomStatusProvider.save_open_status(
      restroom_status_conn,
      restroom=RESTROOM,
      start_date=START_DATE,
      end_date=END_DATE ) is True

   row = restroom_status_conn.execute(
      """   SELECT IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            FROM RestroomStatus
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchone()

   assert tuple( row ) == ( 0, None, START_DATE, END_DATE )


def Test_SaveClosedStatus_TestExistingRow_ExpectUpdatesClosedFields(
      restroom_status_conn: sqlite3.Connection ) -> None:
   RestroomStatusProvider.save_open_status(
      restroom_status_conn,
      restroom=RESTROOM,
      start_date=START_DATE,
      end_date=END_DATE )

   assert RestroomStatusProvider.save_closed_status(
      restroom_status_conn,
      restroom=RESTROOM,
      start_date='2026-07-01',
      end_date='2026-07-15',
      message='Updated closure.' ) is True

   row = restroom_status_conn.execute(
      """   SELECT IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            FROM RestroomStatus
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchone()

   assert tuple( row ) == ( 1, 'Updated closure.', '2026-07-01', '2026-07-15' )
