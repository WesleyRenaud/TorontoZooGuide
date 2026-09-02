from __future__ import annotations

import sqlite3

import pytest

from api.restaurants.data_access.restaurant_provider import RestaurantProvider


RESTAURANT_PROVIDER_SCHEMA = """
CREATE TABLE Restaurant (
   NAME           TEXT NOT NULL PRIMARY KEY,
   LOCATION       TEXT,
   SUB_LOCATION   TEXT,
   DESCRIPTION    TEXT NOT NULL,
   MENU_LINK      TEXT,
   X_COORD        REAL NOT NULL,
   Y_COORD        REAL NOT NULL
);

CREATE TABLE RestaurantDaySeasonalAvailabilityMultiplier (
   RESTAURANT              TEXT    NOT NULL,
   MONTH                   INTEGER NOT NULL,
   DAY                     INTEGER NOT NULL,
   WEEKDAY_VALUE           REAL    NOT NULL,
   WEEKEND_HOLIDAY_VALUE   REAL    NOT NULL,
   PRIMARY KEY ( RESTAURANT, MONTH, DAY )
);

CREATE TABLE RestaurantOpeningSchedule (
   RESTAURANT            TEXT    NOT NULL,
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
   PRIMARY KEY ( RESTAURANT, SCHEDULE_START_DATE )
);

CREATE TABLE RestaurantScheduleOverride (
   RESTAURANT            TEXT    NOT NULL,
   OVERRIDE_START_DATE   TEXT    NOT NULL,
   OVERRIDE_END_DATE     TEXT,
   IS_CLOSED             INTEGER NOT NULL DEFAULT 1,
   OVERRIDE_MESSAGE      TEXT,
   PRIMARY KEY ( RESTAURANT, OVERRIDE_START_DATE )
);
"""

PEACOCK_CAFE = 'Peacock Cafe'
SIMBA_SNACKS = 'Simba Snacks'
VISIT_MONTH = 6
VISIT_DAY = 15


@pytest.fixture
def restaurant_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTAURANT_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_restaurant(
      conn: sqlite3.Connection,
      *,
      name: str,
      location: str | None = 'Africa',
      sub_location: str | None = None,
      menu_link: str | None = None ) -> None:
   conn.execute(
      """   INSERT INTO Restaurant (
               NAME,
               LOCATION,
               SUB_LOCATION,
               DESCRIPTION,
               MENU_LINK,
               X_COORD,
               Y_COORD
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         name,
         location,
         sub_location,
         f'{ name } description',
         menu_link,
         1.0,
         2.0,
      ),
   )


def Test_FetchRestaurantNames_TestEmpty_ExpectEmptyList(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   assert RestaurantProvider.fetch_restaurant_names( restaurant_provider_conn ) == []


def Test_FetchRestaurantNames_TestPopulated_ExpectNames(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   _insert_restaurant( restaurant_provider_conn, name=PEACOCK_CAFE )
   _insert_restaurant( restaurant_provider_conn, name=SIMBA_SNACKS )
   restaurant_provider_conn.commit()

   names = RestaurantProvider.fetch_restaurant_names( restaurant_provider_conn )

   assert set( names ) == { PEACOCK_CAFE, SIMBA_SNACKS }


def Test_FetchRestaurantRecords_TestNoMultiplier_ExpectDefaultMultipliers(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   _insert_restaurant(
      restaurant_provider_conn,
      name=PEACOCK_CAFE,
      sub_location='Near Entrance',
      menu_link='https://example.test/menu' )
   restaurant_provider_conn.commit()

   records = RestaurantProvider.fetch_restaurant_records(
      restaurant_provider_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == PEACOCK_CAFE
   assert record.location == 'Africa'
   assert record.sub_location == 'Near Entrance'
   assert record.description == f'{ PEACOCK_CAFE } description'
   assert record.menu_link == 'https://example.test/menu'
   assert record.x_coord == 1.0
   assert record.y_coord == 2.0
   assert record.weekday_multiplier == 1.0
   assert record.weekend_holiday_multiplier == 1.0


def Test_FetchRestaurantRecords_TestMatchingMultiplier_ExpectJoinedValues(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   _insert_restaurant( restaurant_provider_conn, name=SIMBA_SNACKS )
   restaurant_provider_conn.execute(
      """   INSERT INTO RestaurantDaySeasonalAvailabilityMultiplier (
               RESTAURANT, MONTH, DAY, WEEKDAY_VALUE, WEEKEND_HOLIDAY_VALUE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( SIMBA_SNACKS, VISIT_MONTH, VISIT_DAY, 0.4, 0.8 ),
   )
   restaurant_provider_conn.execute(
      """   INSERT INTO RestaurantDaySeasonalAvailabilityMultiplier (
               RESTAURANT, MONTH, DAY, WEEKDAY_VALUE, WEEKEND_HOLIDAY_VALUE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( SIMBA_SNACKS, 12, 25, 0.1, 0.2 ),
   )
   restaurant_provider_conn.commit()

   records = RestaurantProvider.fetch_restaurant_records(
      restaurant_provider_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   assert records[ 0 ].name == SIMBA_SNACKS
   assert records[ 0 ].weekday_multiplier == 0.4
   assert records[ 0 ].weekend_holiday_multiplier == 0.8


def Test_FetchRestaurantScheduleRecords_TestEmpty_ExpectEmptyList(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   assert RestaurantProvider.fetch_restaurant_schedule_records(
      restaurant_provider_conn ) == []


def Test_FetchRestaurantScheduleRecords_TestPopulated_ExpectMappedFields(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   restaurant_provider_conn.execute(
      """   INSERT INTO RestaurantOpeningSchedule (
               RESTAURANT,
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
            VALUES ( ?, ?, NULL, 0, 0, 0, 0, 0, 1, 1, 1, ? );
      """,
      ( PEACOCK_CAFE, '2026-06-01', 'Weekends and holidays' ),
   )
   restaurant_provider_conn.commit()

   records = RestaurantProvider.fetch_restaurant_schedule_records(
      restaurant_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.restaurant == PEACOCK_CAFE
   assert record.schedule_start_date == '2026-06-01'
   assert record.schedule_end_date is None
   assert record.saturday == 1
   assert record.sunday == 1
   assert record.monday == 0
   assert record.holidays_only == 1
   assert record.schedule_message == 'Weekends and holidays'


def Test_FetchRestaurantScheduleOverrideRecords_TestEmpty_ExpectEmptyList(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   assert RestaurantProvider.fetch_restaurant_schedule_override_records(
      restaurant_provider_conn ) == []


def Test_FetchRestaurantScheduleOverrideRecords_TestPopulated_ExpectMappedFields(
      restaurant_provider_conn: sqlite3.Connection ) -> None:
   restaurant_provider_conn.execute(
      """   INSERT INTO RestaurantScheduleOverride (
               RESTAURANT,
               OVERRIDE_START_DATE,
               OVERRIDE_END_DATE,
               IS_CLOSED,
               OVERRIDE_MESSAGE
            )
            VALUES ( ?, ?, ?, 0, ? );
      """,
      ( PEACOCK_CAFE, '2026-07-04', '2026-07-04', 'Special hours' ),
   )
   restaurant_provider_conn.commit()

   records = RestaurantProvider.fetch_restaurant_schedule_override_records(
      restaurant_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.restaurant == PEACOCK_CAFE
   assert record.override_start_date == '2026-07-04'
   assert record.override_end_date == '2026-07-04'
   assert record.is_closed == 0
   assert record.override_message == 'Special hours'
