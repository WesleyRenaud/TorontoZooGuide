from __future__ import annotations

import sqlite3

import pytest

from api.giftshops.data_access.gift_shop_status_provider import GiftShopStatusProvider
from api.shared.enums.position import Position


GIFT_SHOP = 'Zootique'
OTHER_GIFT_SHOP = 'Courtyard Kiosk'
CLOSED_MESSAGE = 'The Zootique is closed for the season.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
TODAY = '2026-11-02'

GIFT_SHOP_STATUS_SCHEMA = """
CREATE TABLE GiftShopStatus (
   GIFT_SHOP           TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED           INTEGER NOT NULL,
   CLOSED_MESSAGE      TEXT,
   CLOSED_START        TEXT,
   CLOSED_END          TEXT,
   CLOSED_FOR_SEASON   INTEGER NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def gift_shop_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( GIFT_SHOP_STATUS_SCHEMA )

   yield conn

   conn.close()


def _fetch_status_row( conn: sqlite3.Connection, gift_shop: str = GIFT_SHOP ) -> sqlite3.Row:
   return conn.execute(
      """   SELECT
               GIFT_SHOP,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM GiftShopStatus
            WHERE GIFT_SHOP = ?;
      """,
      ( gift_shop, ) ).fetchone()


def Test_SaveClosedForSeason_TestNewGiftShop_ExpectPersistsSeasonRow(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   result = GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   assert result is True
   assert tuple( _fetch_status_row( gift_shop_status_conn ) ) == (
      GIFT_SHOP, 1, CLOSED_MESSAGE, START_DATE, END_DATE, 1 )


def Test_SaveClosedForSeason_TestExistingRow_ExpectReplacesWindow(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date='2026-10-01',
      end_date=None,
      message='Closed until spring.' )

   row = _fetch_status_row( gift_shop_status_conn )

   assert row[ 'CLOSED_START' ] == '2026-10-01'
   assert row[ 'CLOSED_END' ] == None
   assert row[ 'CLOSED_MESSAGE' ] == 'Closed until spring.'
   assert row[ 'CLOSED_FOR_SEASON' ] == 1


def Test_DeleteClosedForSeason_TestExistingRow_ExpectRemoved(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   result = GiftShopStatusProvider.delete_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP )

   assert result is True
   assert _fetch_status_row( gift_shop_status_conn ) == None


def Test_DeleteClosedForSeason_TestMissingRow_ExpectFalse(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   result = GiftShopStatusProvider.delete_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP )

   assert result is False


def Test_FetchClosedForSeasonNames_TestExpiredAndCurrent_ExpectCurrentOnly(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=OTHER_GIFT_SHOP,
      start_date=START_DATE,
      end_date='2026-10-01',
      message=CLOSED_MESSAGE )

   names = GiftShopStatusProvider.fetch_closed_for_season_names(
      gift_shop_status_conn,
      today=TODAY )

   assert names == [ GIFT_SHOP ]


def Test_FetchClosureRecord_TestSavedRow_ExpectMappedRecord(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=None,
      message=CLOSED_MESSAGE )

   record = GiftShopStatusProvider.fetch_closure_record(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP )

   assert record != None
   assert record.gift_shop == GIFT_SHOP
   assert record.closed_start == START_DATE
   assert record.closed_end == None
   assert record.closed_message == CLOSED_MESSAGE
   assert record.is_closed_for_season is True


def Test_FetchClosureRecord_TestMissingGiftShop_ExpectNone(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   record = GiftShopStatusProvider.fetch_closure_record(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP )

   assert record == None


def Test_FetchClosureRecords_TestSavedRows_ExpectAllSeasonClosures(
      gift_shop_status_conn: sqlite3.Connection ) -> None:
   GiftShopStatusProvider.save_closed_for_season(
      gift_shop_status_conn,
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CLOSED_MESSAGE )

   records = GiftShopStatusProvider.fetch_closure_records( gift_shop_status_conn )

   assert len( records ) == 1
   assert records[ Position.FIRST ].gift_shop == GIFT_SHOP
