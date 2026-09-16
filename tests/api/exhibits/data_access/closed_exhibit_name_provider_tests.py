from __future__ import annotations

import sqlite3

import pytest

from api.exhibits.data_access.closed_exhibit_name_provider import ClosedExhibitNameProvider


TODAY = '2026-09-16'
SAVANNA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'
KIDS_ZOO = 'Kids Zoo'

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
def closed_exhibit_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EXHIBIT_STATUS_SCHEMA )

   yield conn

   conn.close()


def _insert_status(
      conn: sqlite3.Connection,
      *,
      exhibit: str,
      is_closed: int,
      start_date: str | None,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO ExhibitStatus (
               EXHIBIT,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         exhibit,
         is_closed,
         'Closed for maintenance.',
         start_date,
         end_date,
      ) )
   conn.commit()


def Test_FetchClosedExhibitNames_TestEmpty_ExpectEmptyList(
      closed_exhibit_name_conn: sqlite3.Connection ) -> None:
   assert ClosedExhibitNameProvider.fetch_closed_exhibit_names(
      closed_exhibit_name_conn,
      TODAY ) == []


def Test_FetchClosedExhibitNames_TestCurrentAndFuture_ExpectDistinctSortedExhibits(
      closed_exhibit_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_exhibit_name_conn,
      exhibit=SAVANNA,
      is_closed=1,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_status(
      closed_exhibit_name_conn,
      exhibit=EURASIA,
      is_closed=1,
      start_date='2026-10-01',
      end_date='2026-10-15' )

   assert ClosedExhibitNameProvider.fetch_closed_exhibit_names(
      closed_exhibit_name_conn,
      TODAY ) == [ SAVANNA, EURASIA ]


def Test_FetchClosedExhibitNames_TestExpired_ExpectExcluded(
      closed_exhibit_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_exhibit_name_conn,
      exhibit=SAVANNA,
      is_closed=1,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert ClosedExhibitNameProvider.fetch_closed_exhibit_names(
      closed_exhibit_name_conn,
      TODAY ) == []


def Test_FetchClosedExhibitNames_TestEndingToday_ExpectIncluded(
      closed_exhibit_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_exhibit_name_conn,
      exhibit=SAVANNA,
      is_closed=1,
      start_date='2026-09-01',
      end_date=TODAY )

   assert ClosedExhibitNameProvider.fetch_closed_exhibit_names(
      closed_exhibit_name_conn,
      TODAY ) == [ SAVANNA ]


def Test_FetchClosedExhibitNames_TestOpenRow_ExpectExcluded(
      closed_exhibit_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_exhibit_name_conn,
      exhibit=KIDS_ZOO,
      is_closed=0,
      start_date='2026-09-01',
      end_date=None )

   assert ClosedExhibitNameProvider.fetch_closed_exhibit_names(
      closed_exhibit_name_conn,
      TODAY ) == []
