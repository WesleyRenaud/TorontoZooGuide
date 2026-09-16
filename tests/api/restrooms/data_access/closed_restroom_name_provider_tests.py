from __future__ import annotations

import sqlite3

import pytest

from api.restrooms.data_access.closed_restroom_name_provider import ClosedRestroomNameProvider


TODAY = '2026-09-16'
AFRICA = 'Africa Restaurant Restroom'
ENTRANCE = 'Entrance Restroom'
SPLASH = 'Splash Island Restroom'

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
def closed_restroom_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTROOM_STATUS_SCHEMA )

   yield conn

   conn.close()


def _insert_status(
      conn: sqlite3.Connection,
      *,
      restroom: str,
      is_closed: int,
      start_date: str | None,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO RestroomStatus (
               RESTROOM,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         restroom,
         is_closed,
         'Closed for maintenance.',
         start_date,
         end_date,
      ) )
   conn.commit()


def Test_FetchClosedRestroomNames_TestEmpty_ExpectEmptyList(
      closed_restroom_name_conn: sqlite3.Connection ) -> None:
   assert ClosedRestroomNameProvider.fetch_closed_restroom_names(
      closed_restroom_name_conn,
      TODAY ) == []


def Test_FetchClosedRestroomNames_TestCurrentAndFuture_ExpectDistinctSortedRestrooms(
      closed_restroom_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_restroom_name_conn,
      restroom=AFRICA,
      is_closed=1,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_status(
      closed_restroom_name_conn,
      restroom=ENTRANCE,
      is_closed=1,
      start_date='2026-10-01',
      end_date='2026-10-15' )

   assert ClosedRestroomNameProvider.fetch_closed_restroom_names(
      closed_restroom_name_conn,
      TODAY ) == [ AFRICA, ENTRANCE ]


def Test_FetchClosedRestroomNames_TestExpired_ExpectExcluded(
      closed_restroom_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_restroom_name_conn,
      restroom=AFRICA,
      is_closed=1,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert ClosedRestroomNameProvider.fetch_closed_restroom_names(
      closed_restroom_name_conn,
      TODAY ) == []


def Test_FetchClosedRestroomNames_TestEndingToday_ExpectIncluded(
      closed_restroom_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_restroom_name_conn,
      restroom=AFRICA,
      is_closed=1,
      start_date='2026-09-01',
      end_date=TODAY )

   assert ClosedRestroomNameProvider.fetch_closed_restroom_names(
      closed_restroom_name_conn,
      TODAY ) == [ AFRICA ]


def Test_FetchClosedRestroomNames_TestOpenRow_ExpectExcluded(
      closed_restroom_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_restroom_name_conn,
      restroom=SPLASH,
      is_closed=0,
      start_date='2026-09-01',
      end_date=None )

   assert ClosedRestroomNameProvider.fetch_closed_restroom_names(
      closed_restroom_name_conn,
      TODAY ) == []
