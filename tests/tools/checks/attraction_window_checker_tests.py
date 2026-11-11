from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.attraction_window_checker import AttractionWindowChecker as CHECKER
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.opening_window import OpeningWindow
from tools.checks.website_page import WebsitePage
from tools.checks.weekday_window import WeekdayWindow


ZOOM = 'Zoomobile'
SPLASH = 'Splash Island'
TODAY = date( 2026, 11, 9 )
SCHEMA = """
CREATE TABLE Attraction (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   INFO_LINK            TEXT NOT NULL,
   WEEKDAY_START_MONTH  INTEGER,
   WEEKDAY_END_MONTH    INTEGER,
   WEEKEND_START_MONTH  INTEGER,
   WEEKEND_END_MONTH    INTEGER
);

CREATE TABLE AttractionOpeningSchedule (
   ATTRACTION           TEXT NOT NULL,
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
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);
"""


def _write_database(
      path: Path,
      schedules: list[ tuple[ str, str, str | None, list[ int ], int ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Attraction ( NAME, INFO_LINK ) VALUES ( ?, ? )',
      [
         ( ZOOM, 'https://www.torontozoo.com/tickets/zoomobile' ),
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
      ],
   )

   for name, start, end, days, holidays in schedules:
      connection.execute(
         """   INSERT INTO AttractionOpeningSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY
               ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
         """,
         ( name, start, end, *days, holidays ),
      )

   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str, str ] ] ) -> str:
   return ''.join(
      f'<a class="col3" href="{ href }">'
      f'<div class="col3title">{ title }</div>'
      f'<span class="opentxt">{ status }</span>'
      '</a>'
      for href, title, status in cards
   )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _rows( database: Path, name: str ) -> list[ sqlite3.Row ]:
   connection = sqlite3.connect( database )
   connection.row_factory = sqlite3.Row
   rows = connection.execute(
      """   SELECT *
            FROM AttractionOpeningSchedule
            WHERE ATTRACTION = ?
            ORDER BY SCHEDULE_START_DATE
      """,
      ( name, ),
   ).fetchall()
   connection.close()
   return rows


def _check(
      database: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, TODAY )
   return result, capsys.readouterr().out


def Test_CheckSchedules_TestWeekendHolidayMismatch_ExpectNoEnd(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( ZOOM, '2026-01-01', '2026-12-31', [ 1, 1, 1, 1, 1, 1, 1 ], 0 ),
         ( SPLASH, '2026-01-01', '2026-12-31', [ 1, 0, 0, 0, 0, 0, 0 ], 0 ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( 'https://www.torontozoo.com/tickets/zoomobile', ZOOM, 'Open Weekends & Holidays' ),
         ( 'https://www.torontozoo.com/tz/kidszoo', 'Kids Zoo', 'Open Daily' ),
         ( 'https://www.torontozoo.com/tz/splash', SPLASH, 'Closed for the Season' ),
      ] ),
   )
   pattern = WeekdayWindow.parse( 'Open Weekends & Holidays' )
   detail = OpeningWindow.detail( OpeningWindow( TODAY, None, pattern ) )

   result, output = _check( database, capsys )
   rows = _rows( database, ZOOM )

   assert result == 0
   assert ExhibitRegionColors.listed_region( ZOOM ) in output
   assert detail in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == None
   assert rows[ 0 ][ 'SATURDAY' ] == 1
   assert rows[ 0 ][ 'SUNDAY' ] == 1
   assert rows[ 0 ][ 'MONDAY' ] == 0
   assert rows[ 0 ][ 'HOLIDAYS_ONLY' ] == 1
   assert _rows( database, SPLASH )[ 0 ][ 'MONDAY' ] == 1
   assert CheckReport.fixed_count == 1


def Test_CheckSchedules_TestWindowEndingTomorrow_ExpectNoEnd(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   tomorrow = TODAY + timedelta( days=1 )
   _write_database(
      database,
      [ ( ZOOM, '2026-01-01', tomorrow.isoformat(), [ 1, 1, 1, 1, 1, 1, 1 ], 0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( 'https://www.torontozoo.com/tickets/zoomobile', ZOOM, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, capsys )
   rows = _rows( database, ZOOM )

   assert result == 0
   assert OpeningWindow.detail( OpeningWindow(
      date( 2026, 1, 1 ),
      None,
      WeekdayWindow.parse( 'Open Daily' ),
   ) ) in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == '2026-01-01'
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == None


def Test_CheckSchedules_TestMatchingDaysPastTwoWeeks_ExpectNoEnd(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( ZOOM, '2026-01-01', '2026-12-31', [ 1, 1, 1, 1, 1, 1, 1 ], 0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( 'https://www.torontozoo.com/tickets/zoomobile', ZOOM, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, capsys )
   rows = _rows( database, ZOOM )

   assert result == 0
   assert OpeningWindow.detail( OpeningWindow(
      date( 2026, 1, 1 ),
      None,
      WeekdayWindow.parse( 'Open Daily' ),
   ) ) in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == '2026-01-01'
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == None
