from __future__ import annotations

import sqlite3

import pytest

from api.giftshops.data_access.gift_shop_provider import GiftShopProvider


GIFT_SHOP_PROVIDER_SCHEMA = """
CREATE TABLE GiftShop (
   NAME          TEXT NOT NULL PRIMARY KEY,
   LOCATION      TEXT NOT NULL,
   DESCRIPTION   TEXT NOT NULL,
   X_COORD       REAL NOT NULL,
   Y_COORD       REAL NOT NULL
);

CREATE TABLE GiftShopDaySeasonalAvailabilityMultiplier (
   GIFT_SHOP               TEXT    NOT NULL,
   MONTH                   INTEGER NOT NULL,
   DAY                     INTEGER NOT NULL,
   WEEKDAY_VALUE           REAL    NOT NULL,
   WEEKEND_HOLIDAY_VALUE   REAL    NOT NULL,
   PRIMARY KEY ( GIFT_SHOP, MONTH, DAY )
);

CREATE TABLE GiftShopOpeningSchedule (
   GIFT_SHOP             TEXT    NOT NULL,
   SCHEDULE_START_DATE   TEXT    NOT NULL,
   SCHEDULE_END_DATE     TEXT,
   MONDAY                INTEGER NOT NULL DEFAULT 0,
   TUESDAY               INTEGER NOT NULL DEFAULT 0,
   WEDNESDAY             INTEGER NOT NULL DEFAULT 0,
   THURSDAY              INTEGER NOT NULL DEFAULT 0,
   FRIDAY                INTEGER NOT NULL DEFAULT 0,
   SATURDAY              INTEGER NOT NULL DEFAULT 0,
   SUNDAY                INTEGER NOT NULL DEFAULT 0,
   HOLIDAYS_ONLY         INTEGER NOT NULL DEFAULT 0,
   SCHEDULE_MESSAGE      TEXT,
   PRIMARY KEY ( GIFT_SHOP, SCHEDULE_START_DATE )
);

CREATE TABLE GiftShopScheduleOverride (
   GIFT_SHOP             TEXT    NOT NULL,
   OVERRIDE_START_DATE   TEXT    NOT NULL,
   OVERRIDE_END_DATE     TEXT,
   IS_CLOSED             INTEGER NOT NULL DEFAULT 1,
   OVERRIDE_MESSAGE      TEXT,
   PRIMARY KEY ( GIFT_SHOP, OVERRIDE_START_DATE )
);
"""

ZOO_SHOP = 'Zoo Shop'
SAVANNA_STORE = 'Savanna Store'
VISIT_MONTH = 6
VISIT_DAY = 15


@pytest.fixture
def gift_shop_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( GIFT_SHOP_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_gift_shop(
      conn: sqlite3.Connection,
      *,
      name: str,
      location: str = 'Main Entrance' ) -> None:
   conn.execute(
      """   INSERT INTO GiftShop (
               NAME,
               LOCATION,
               DESCRIPTION,
               X_COORD,
               Y_COORD
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( name, location, f'{ name } description', 3.0, 4.0 ),
   )


def Test_FetchGiftShopNames_TestEmpty_ExpectEmptyList(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   assert GiftShopProvider.fetch_gift_shop_names( gift_shop_provider_conn ) == []


def Test_FetchGiftShopNames_TestPopulated_ExpectNames(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   _insert_gift_shop( gift_shop_provider_conn, name=ZOO_SHOP )
   _insert_gift_shop(
      gift_shop_provider_conn,
      name=SAVANNA_STORE,
      location='Africa' )
   gift_shop_provider_conn.commit()

   names = GiftShopProvider.fetch_gift_shop_names( gift_shop_provider_conn )

   assert set( names ) == { ZOO_SHOP, SAVANNA_STORE }


def Test_FetchGiftShopRecords_TestNoMultiplier_ExpectDefaultMultipliers(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   _insert_gift_shop( gift_shop_provider_conn, name=ZOO_SHOP )
   gift_shop_provider_conn.commit()

   records = GiftShopProvider.fetch_gift_shop_records(
      gift_shop_provider_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == ZOO_SHOP
   assert record.location == 'Main Entrance'
   assert record.description == f'{ ZOO_SHOP } description'
   assert record.x_coord == 3.0
   assert record.y_coord == 4.0
   assert record.weekday_multiplier == 1.0
   assert record.weekend_holiday_multiplier == 1.0


def Test_FetchGiftShopRecords_TestMatchingMultiplier_ExpectJoinedValues(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   _insert_gift_shop(
      gift_shop_provider_conn,
      name=SAVANNA_STORE,
      location='Africa' )
   gift_shop_provider_conn.execute(
      """   INSERT INTO GiftShopDaySeasonalAvailabilityMultiplier (
               GIFT_SHOP, MONTH, DAY, WEEKDAY_VALUE, WEEKEND_HOLIDAY_VALUE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( SAVANNA_STORE, VISIT_MONTH, VISIT_DAY, 0.6, 0.9 ),
   )
   gift_shop_provider_conn.commit()

   records = GiftShopProvider.fetch_gift_shop_records(
      gift_shop_provider_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   assert records[ 0 ].name == SAVANNA_STORE
   assert records[ 0 ].weekday_multiplier == 0.6
   assert records[ 0 ].weekend_holiday_multiplier == 0.9


def Test_FetchGiftShopScheduleRecords_TestEmpty_ExpectEmptyList(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   assert GiftShopProvider.fetch_gift_shop_schedule_records(
      gift_shop_provider_conn ) == []


def Test_FetchGiftShopScheduleRecords_TestPopulated_ExpectMappedFields(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   gift_shop_provider_conn.execute(
      """   INSERT INTO GiftShopOpeningSchedule (
               GIFT_SHOP,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               HOLIDAYS_ONLY,
               SCHEDULE_MESSAGE
            )
            VALUES ( ?, ?, ?, 1, 1, 1, 1, 1, 1, 1, 0, ? );
      """,
      ( ZOO_SHOP, '2026-04-01', '2026-10-31', 'Open daily in season' ),
   )
   gift_shop_provider_conn.commit()

   records = GiftShopProvider.fetch_gift_shop_schedule_records(
      gift_shop_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.gift_shop == ZOO_SHOP
   assert record.schedule_start_date == '2026-04-01'
   assert record.schedule_end_date == '2026-10-31'
   assert record.monday == 1
   assert record.sunday == 1
   assert record.holidays_only == 0
   assert record.schedule_message == 'Open daily in season'


def Test_FetchGiftShopScheduleOverrideRecords_TestEmpty_ExpectEmptyList(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   assert GiftShopProvider.fetch_gift_shop_schedule_override_records(
      gift_shop_provider_conn ) == []


def Test_FetchGiftShopScheduleOverrideRecords_TestPopulated_ExpectMappedFields(
      gift_shop_provider_conn: sqlite3.Connection ) -> None:
   gift_shop_provider_conn.execute(
      """   INSERT INTO GiftShopScheduleOverride (
               GIFT_SHOP,
               OVERRIDE_START_DATE,
               OVERRIDE_END_DATE,
               IS_CLOSED,
               OVERRIDE_MESSAGE
            )
            VALUES ( ?, ?, NULL, 1, ? );
      """,
      ( ZOO_SHOP, '2026-12-25', 'Closed for holiday' ),
   )
   gift_shop_provider_conn.commit()

   records = GiftShopProvider.fetch_gift_shop_schedule_override_records(
      gift_shop_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.gift_shop == ZOO_SHOP
   assert record.override_start_date == '2026-12-25'
   assert record.override_end_date is None
   assert record.is_closed == 1
   assert record.override_message == 'Closed for holiday'
