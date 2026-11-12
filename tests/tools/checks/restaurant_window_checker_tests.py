from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.shared.calendar_dates import CalendarDates
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.opening_window import OpeningWindow
from tools.checks.restaurant_window_checker import RestaurantWindowChecker as CHECKER
from tools.checks.website_page import WebsitePage
from tools.checks.weekday_window import WeekdayWindow


COCOA = 'Cocoa Flow'
WOLF = "Wolf's Den Café"
TODAY = date( 2026, 11, 9 )
SCHEMA = """
CREATE TABLE Restaurant (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   WEEKDAY_START_MONTH  INTEGER,
   WEEKDAY_END_MONTH    INTEGER,
   WEEKEND_START_MONTH  INTEGER,
   WEEKEND_END_MONTH    INTEGER
);

CREATE TABLE RestaurantOpeningSchedule (
   RESTAURANT           TEXT NOT NULL,
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
   PRIMARY KEY ( RESTAURANT, SCHEDULE_START_DATE )
);
"""


def _write_database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.execute(
      """   INSERT INTO Restaurant (
               NAME,
               WEEKDAY_START_MONTH,
               WEEKDAY_END_MONTH,
               WEEKEND_START_MONTH,
               WEEKEND_END_MONTH
            ) VALUES ( ?, 6, 8, 5, 10 )
      """,
      ( COCOA, ),
   )
   connection.execute(
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
               SUNDAY
            ) VALUES ( ?, '2026-01-01', '2026-12-31', 1, 1, 1, 1, 1, 1, 1 )
      """,
      ( COCOA, ),
   )
   connection.commit()
   connection.close()


def _wolf_database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.execute(
      """   INSERT INTO Restaurant (
               NAME,
               WEEKDAY_START_MONTH,
               WEEKDAY_END_MONTH,
               WEEKEND_START_MONTH,
               WEEKEND_END_MONTH
            ) VALUES ( ?, 6, 8, 5, 10 )
      """,
      ( WOLF, ),
   )
   connection.commit()
   connection.close()


def _wolf_page() -> str:
   return (
      '<a class="col3" href="https://www.torontozoo.com/tz/wolfsden">'
      '<div class="col3title">Wolf&#39;s Den Café</div>'
      '<font color="#ac208d"><b>Weekends</b></font>'
      '</a>'
   )


def _page() -> str:
   return (
      '<a class="col3" href="https://www.torontozoo.com/tz/cocoa">'
      '<div class="col3title">Cocoa Flow</div>'
      '<span class="opentxt">Thursday to Sunday</span>'
      '</a>'
      '<a class="col3" href="https://www.torontozoo.com/tz/carts">'
      '<div class="col3title">Ice Cream Carts</div>'
      '<span class="opentxt">Open Daily</span>'
      '</a>'
   )


def Test_CheckSchedules_TestThursdayToSunday_ExpectTwoWeekWindow(
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
   row = connection.execute(
      'SELECT * FROM RestaurantOpeningSchedule WHERE RESTAURANT = ?',
      ( COCOA, ),
   ).fetchone()
   connection.close()

   assert result == 0
   assert ExhibitRegionColors.restaurant_label( COCOA ) in output
   assert OpeningWindow.detail( OpeningWindow(
      TODAY,
      CalendarDates.two_weeks_later( TODAY ),
      WeekdayWindow.parse( 'Thursday to Sunday' ),
   ) ) in output
   assert row[ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
   assert row[ 'SCHEDULE_END_DATE' ] == CalendarDates.two_weeks_later( TODAY ).isoformat()
   assert row[ 'WEDNESDAY' ] == 0
   assert row[ 'THURSDAY' ] == 1
   assert row[ 'SUNDAY' ] == 1
   assert row[ 'HOLIDAYS_ONLY' ] == 0
   assert CheckReport.fixed_count == 1


def Test_CheckSchedules_TestFontWeekends_ExpectWeekendWindow(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _wolf_database( database )

   def fetch_text( url: str ) -> str:
      return _wolf_page()

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )
   output = capsys.readouterr().out
   connection = sqlite3.connect( database )
   connection.row_factory = sqlite3.Row
   row = connection.execute(
      'SELECT * FROM RestaurantOpeningSchedule WHERE RESTAURANT = ?',
      ( WOLF, ),
   ).fetchone()
   connection.close()

   assert result == 0
   assert ExhibitRegionColors.restaurant_label( WOLF ) in output
   assert row[ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
   assert row[ 'SCHEDULE_END_DATE' ] == CalendarDates.two_weeks_later( TODAY ).isoformat()
   assert row[ 'FRIDAY' ] == 0
   assert row[ 'SATURDAY' ] == 1
   assert row[ 'SUNDAY' ] == 1
   assert row[ 'HOLIDAYS_ONLY' ] == 0
