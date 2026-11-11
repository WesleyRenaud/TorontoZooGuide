from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.shared.calendar_dates import CalendarDates
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.gift_shop_window_checker import GiftShopWindowChecker as CHECKER
from tools.checks.opening_window import OpeningWindow
from tools.checks.website_page import WebsitePage
from tools.checks.weekday_window import WeekdayWindow


SAVANNA = 'Savanna Shop'
ZOOTIQUE = 'Zootique'
OUTPOST = 'Eurasia Wilds Outpost'
TODAY = date( 2026, 11, 9 )
SCHEMA = """
CREATE TABLE GiftShop (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   WEEKDAY_START_MONTH  INTEGER,
   WEEKDAY_END_MONTH    INTEGER,
   WEEKEND_START_MONTH  INTEGER,
   WEEKEND_END_MONTH    INTEGER
);

CREATE TABLE GiftShopOpeningSchedule (
   GIFT_SHOP            TEXT NOT NULL,
   SCHEDULE_START_DATE  DATE NOT NULL,
   SCHEDULE_END_DATE    DATE,
   MONDAY               BOOL NOT NULL DEFAULT 0,
   TUESDAY              BOOL NOT NULL DEFAULT 0,
   WEDNESDAY            BOOL NOT NULL DEFAULT 0,
   THURSDAY             BOOL NOT NULL DEFAULT 0,
   FRIDAY               BOOL NOT NULL DEFAULT 0,
   SATURDAY             BOOL NOT NULL DEFAULT 0,
   SUNDAY               BOOL NOT NULL DEFAULT 0,
   HOLIDAYS_ONLY        BOOL NOT NULL DEFAULT 0,
   SCHEDULE_MESSAGE     TEXT,
   PRIMARY KEY ( GIFT_SHOP, SCHEDULE_START_DATE )
);
"""


def _write_database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.execute(
      """   INSERT INTO GiftShop (
               NAME,
               WEEKDAY_START_MONTH,
               WEEKDAY_END_MONTH,
               WEEKEND_START_MONTH,
               WEEKEND_END_MONTH
            ) VALUES ( ?, 6, 8, 5, 10 )
      """,
      ( SAVANNA, ),
   )
   connection.execute( 'INSERT INTO GiftShop ( NAME ) VALUES ( ? )', ( ZOOTIQUE, ) )
   connection.execute(
      """   INSERT INTO GiftShop (
               NAME,
               WEEKDAY_START_MONTH,
               WEEKDAY_END_MONTH,
               WEEKEND_START_MONTH,
               WEEKEND_END_MONTH
            ) VALUES ( ?, 6, 8, 5, 10 )
      """,
      ( OUTPOST, ),
   )
   connection.execute(
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
               SUNDAY
            ) VALUES ( ?, '2026-01-01', '2026-12-31', 1, 1, 1, 1, 1, 1, 1 )
      """,
      ( ZOOTIQUE, ),
   )
   connection.execute(
      """   INSERT INTO GiftShopOpeningSchedule (
               GIFT_SHOP,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY
            ) VALUES ( ?, '2026-01-01', '2026-12-31', 1 )
      """,
      ( OUTPOST, ),
   )
   connection.commit()
   connection.close()


def _page() -> str:
   shops = [
      ( SAVANNA, 'Open Weekends' ),
      ( ZOOTIQUE, 'Open Daily' ),
      ( OUTPOST, 'Closed for the Season' ),
   ]
   return ''.join(
      f'<div class="col3"><strong>{ title }</strong>'
      f'<span class="opentxt">{ status }</span></div>'
      for title, status in shops
   )


def Test_CheckSchedules_TestWeekendsWithoutSchedule_ExpectTwoWeekWindow(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database )

   def fetch_text( url: str ) -> str:
      return _page()

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )
   output = capsys.readouterr().out
   connection = sqlite3.connect( database )
   connection.row_factory = sqlite3.Row
   savanna = connection.execute(
      'SELECT * FROM GiftShopOpeningSchedule WHERE GIFT_SHOP = ?',
      ( SAVANNA, ),
   ).fetchone()
   outpost = connection.execute(
      'SELECT MONDAY, SCHEDULE_END_DATE FROM GiftShopOpeningSchedule WHERE GIFT_SHOP = ?',
      ( OUTPOST, ),
   ).fetchone()
   zootique = connection.execute(
      'SELECT SCHEDULE_START_DATE, SCHEDULE_END_DATE FROM GiftShopOpeningSchedule WHERE GIFT_SHOP = ?',
      ( ZOOTIQUE, ),
   ).fetchone()
   connection.close()

   assert result == 0
   assert ExhibitRegionColors.gift_shop_label( SAVANNA ) in output
   assert OpeningWindow.detail( OpeningWindow(
      TODAY,
      CalendarDates.two_weeks_later( TODAY ),
      WeekdayWindow.parse( 'Open Weekends' ),
   ) ) in output
   assert savanna[ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
   assert savanna[ 'SCHEDULE_END_DATE' ] == CalendarDates.two_weeks_later( TODAY ).isoformat()
   assert savanna[ 'FRIDAY' ] == 0
   assert savanna[ 'SATURDAY' ] == 1
   assert savanna[ 'SUNDAY' ] == 1
   assert savanna[ 'HOLIDAYS_ONLY' ] == 0
   assert outpost[ 'MONDAY' ] == 1
   assert outpost[ 'SCHEDULE_END_DATE' ] == '2026-12-31'
   assert zootique[ 'SCHEDULE_START_DATE' ] == '2026-01-01'
   assert zootique[ 'SCHEDULE_END_DATE' ] == None
   assert CheckReport.fixed_count == 2
