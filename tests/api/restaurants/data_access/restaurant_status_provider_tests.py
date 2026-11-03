from __future__ import annotations

import sqlite3

import pytest

from api.restaurants.data_access.restaurant_status_provider import RestaurantStatusProvider
from api.shared.enums.position import Position


RESTAURANT = 'Africa Restaurant'
OTHER_RESTAURANT = 'Beavertails'
CLOSED_MESSAGE = 'The Africa Restaurant is closed for the season.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
TODAY = '2026-11-02'

RESTAURANT_STATUS_SCHEMA = """
CREATE TABLE RestaurantStatus (
   RESTAURANT          TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED           INTEGER NOT NULL,
   CLOSED_MESSAGE      TEXT,
   CLOSED_START        TEXT,
   CLOSED_END          TEXT,
   CLOSED_FOR_SEASON   INTEGER NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def restaurant_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTAURANT_STATUS_SCHEMA )

   yield conn

   conn.close()


def _fetch_status_row( conn: sqlite3.Connection, restaurant: str = RESTAURANT ) -> sqlite3.Row:
   return conn.execute(
      """   SELECT
               RESTAURANT,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM RestaurantStatus
            WHERE RESTAURANT = ?;
      """,
      ( restaurant, ) ).fetchone()


def Test_SaveClosedForSeason_TestNewRestaurant_ExpectPersistsSeasonRow(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   result = RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   assert result is True
   assert tuple( _fetch_status_row( restaurant_status_conn ) ) == (
      RESTAURANT, 1, CLOSED_MESSAGE, START_DATE, END_DATE, 1 )


def Test_SaveClosedForSeason_TestExistingRow_ExpectReplacesWindow(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date='2026-10-01',
      end_date=None,
      message='Closed until spring.' )

   row = _fetch_status_row( restaurant_status_conn )

   assert row[ 'CLOSED_START' ] == '2026-10-01'
   assert row[ 'CLOSED_END' ] == None
   assert row[ 'CLOSED_MESSAGE' ] == 'Closed until spring.'
   assert row[ 'CLOSED_FOR_SEASON' ] == 1


def Test_DeleteClosedForSeason_TestExistingRow_ExpectRemoved(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   result = RestaurantStatusProvider.delete_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT )

   assert result is True
   assert _fetch_status_row( restaurant_status_conn ) == None


def Test_DeleteClosedForSeason_TestMissingRow_ExpectFalse(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   result = RestaurantStatusProvider.delete_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT )

   assert result is False


def Test_FetchClosedForSeasonNames_TestExpiredAndCurrent_ExpectCurrentOnly(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=OTHER_RESTAURANT,
      start_date=START_DATE,
      end_date='2026-10-01',
      message=CLOSED_MESSAGE )

   names = RestaurantStatusProvider.fetch_closed_for_season_names(
      restaurant_status_conn,
      today=TODAY )

   assert names == [ RESTAURANT ]


def Test_FetchClosureRecord_TestSavedRow_ExpectMappedRecord(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   record = RestaurantStatusProvider.fetch_closure_record(
      restaurant_status_conn,
      restaurant=RESTAURANT )

   assert record != None
   assert record.restaurant == RESTAURANT
   assert record.closed_start == START_DATE
   assert record.closed_end == None
   assert record.closed_message == CLOSED_MESSAGE
   assert record.is_closed_for_season is True


def Test_FetchClosureRecord_TestMissingRestaurant_ExpectNone(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   record = RestaurantStatusProvider.fetch_closure_record(
      restaurant_status_conn,
      restaurant=RESTAURANT )

   assert record == None


def Test_FetchClosureRecords_TestSavedRows_ExpectAllSeasonClosures(
      restaurant_status_conn: sqlite3.Connection ) -> None:
   RestaurantStatusProvider.save_closed_for_season(
      restaurant_status_conn,
      restaurant=RESTAURANT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   records = RestaurantStatusProvider.fetch_closure_records( restaurant_status_conn )

   assert len( records ) == 1
   assert records[ Position.FIRST ].restaurant == RESTAURANT
