from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.attraction_hours_reader import AttractionHoursReader
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

CREATE TABLE AttractionHoursSchedule (
   ATTRACTION                      TEXT NOT NULL,
   SCHEDULE_START_DATE             DATE NOT NULL,
   SCHEDULE_END_DATE               DATE,
   WEEKDAY_START_TIME              VARCHAR(16) NOT NULL,
   WEEKDAY_END_TIME                VARCHAR(16) NOT NULL,
   WEEKEND_HOLIDAY_START_TIME      VARCHAR(16) NOT NULL,
   WEEKEND_HOLIDAY_END_TIME        VARCHAR(16) NOT NULL,
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


HOURS_DAY = date( 2026, 9, 1 )
SEASON_END = '2026-10-31'
ZOOM = 'Zoomobile'
SPLASH = 'Splash Island'
GREENHOUSE = 'Greenhouse'
DAILY = [ 1, 1, 1, 1, 1, 1, 1 ]
WEEKEND = [ 0, 0, 0, 0, 0, 1, 1 ]
HOURS_SCHEMA = """
CREATE TABLE ZooHours (
   OPERATING_DATE        DATE NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME  VARCHAR(5),
   OPEN_TIME             VARCHAR(5) NOT NULL,
   LAST_ADMISSION_TIME   VARCHAR(5) NOT NULL,
   CLOSE_TIME            VARCHAR(5) NOT NULL
);

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

CREATE TABLE AttractionHoursSchedule (
   ATTRACTION                      TEXT NOT NULL,
   SCHEDULE_START_DATE             DATE NOT NULL,
   SCHEDULE_END_DATE               DATE,
   WEEKDAY_START_TIME              VARCHAR(16) NOT NULL,
   WEEKDAY_END_TIME                VARCHAR(16) NOT NULL,
   WEEKEND_HOLIDAY_START_TIME      VARCHAR(16) NOT NULL,
   WEEKEND_HOLIDAY_END_TIME        VARCHAR(16) NOT NULL,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);
"""


def _hours_card( title: str, status: str, extra: str = '' ) -> str:
   return (
      f'<a class="col3" href="/tz/{ title }">'
      f'<div class="col3title">{ title }</div>'
      f'<span class="opentxt">{ status }</span>{ extra }</a>'
   )


def _write_hours(
      path: Path,
      names: list[ str ],
      hours: list[ tuple[ str, str, str | None, str, str, str, str ] ],
      openings: list[ tuple[ str, list[ int ], int ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( HOURS_SCHEMA )
   connection.executemany(
      """   INSERT INTO Attraction (
               NAME,
               INFO_LINK,
               WEEKDAY_START_MONTH,
               WEEKDAY_END_MONTH,
               WEEKEND_START_MONTH,
               WEEKEND_END_MONTH
            ) VALUES ( ?, ?, 5, 10, 5, 10 )
      """,
      [ ( name, f'/tz/{ name }' ) for name in names ],
   )

   for name, days, holidays in openings:
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
               ) VALUES ( ?, '2026-07-29', ?, ?, ?, ?, ?, ?, ?, ?, ? )
         """,
         ( name, SEASON_END, *days, holidays ),
      )
   connection.executemany(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            ) VALUES ( ?, '08:30', '09:00', '18:00', '19:00' )
      """,
      [ ( '2026-09-01', ), ( '2026-09-05', ) ],
   )
   connection.executemany(
      """   INSERT INTO AttractionHoursSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? )
      """,
      hours,
   )
   connection.commit()
   connection.close()


def _hour_rows( database: Path, name: str ) -> list[ sqlite3.Row ]:
   connection = sqlite3.connect( database )
   connection.row_factory = sqlite3.Row
   rows = connection.execute(
      """   SELECT *
            FROM AttractionHoursSchedule
            WHERE ATTRACTION = ?
            ORDER BY SCHEDULE_START_DATE
      """,
      ( name, ),
   ).fetchall()
   connection.close()
   return rows


def _check_hours(
      database: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, HOURS_DAY )
   return result, capsys.readouterr().out



def _prepare_christmas( database: Path ) -> None:
   connection = sqlite3.connect( database )
   connection.execute(
      """   UPDATE Attraction
            SET WEEKDAY_END_MONTH = 12,
                WEEKEND_END_MONTH = 12
      """
   )
   connection.execute(
      """   UPDATE AttractionOpeningSchedule
            SET SCHEDULE_END_DATE = '2026-12-31'
      """
   )
   connection.executemany(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            ) VALUES ( ?, '08:30', ?, '18:00', ? )
      """,
      [
         ( '2026-11-16', '09:00', '19:00' ),
         ( '2026-11-21', '09:00', '19:00' ),
         ( '2026-12-25', '11:00', '16:00' ),
         ( '2026-12-26', '09:00', '19:00' ),
         ( '2026-12-28', '09:00', '19:00' ),
      ],
   )
   connection.commit()
   connection.close()


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
      TODAY,
      None,
      WeekdayWindow.parse( 'Open Daily' ),
   ) ) in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
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
      TODAY,
      None,
      WeekdayWindow.parse( 'Open Daily' ),
   ) ) in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == TODAY.isoformat()
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == None


def Test_CheckSchedules_TestBothPairs_ExpectWrittenHours(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours( database, [ ZOOM ], [], [ ( ZOOM, DAILY, 0 ) ] )
   _install_page(
      monkeypatch,
      _hours_card(
         ZOOM,
         'Open Daily',
         '<strong>Weekdays: 10:00am - 4:00pm Weekends/Holidays: 10:00am - 5:30pm</strong>',
      ),
   )

   result, output = _check_hours( database, capsys )
   rows = _hour_rows( database, ZOOM )

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert '10:00 AM to 4:00 PM on weekdays and 10:00 AM to 5:30 PM on weekends and holidays' in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == HOURS_DAY.isoformat()
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == SEASON_END
   assert rows[ 0 ][ 'WEEKDAY_START_TIME' ] == '10:00 AM'
   assert rows[ 0 ][ 'WEEKDAY_END_TIME' ] == '4:00 PM'
   assert rows[ 0 ][ 'WEEKEND_HOLIDAY_START_TIME' ] == '10:00 AM'
   assert rows[ 0 ][ 'WEEKEND_HOLIDAY_END_TIME' ] == '5:30 PM'


def Test_CheckSchedules_TestMatchingHours_ExpectNoWrite(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ ZOOM ],
      [ ( ZOOM, '2026-07-29', SEASON_END, '10:00 AM', '4:00 PM', '10:00 AM', '5:30 PM' ) ],
      [ ( ZOOM, DAILY, 0 ) ],
   )
   _install_page(
      monkeypatch,
      _hours_card(
         ZOOM,
         'Open Daily',
         '<strong>Weekdays: 10:00am - 4:00pm Weekends/Holidays: 10:00am - 5:30pm</strong>',
      ),
   )

   result, output = _check_hours( database, capsys )
   rows = _hour_rows( database, ZOOM )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert 'Set the attraction hours' not in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == '2026-07-29'


def Test_CheckSchedules_TestEarlierEnd_ExpectExtended(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ ZOOM ],
      [ ( ZOOM, '2026-07-29', '2026-09-07', '10:00 AM', '4:00 PM', '10:00 AM', '5:30 PM' ) ],
      [ ( ZOOM, DAILY, 0 ) ],
   )
   _install_page(
      monkeypatch,
      _hours_card(
         ZOOM,
         'Open Daily',
         '<strong>Weekdays: 10:00am - 4:00pm Weekends/Holidays: 10:00am - 5:30pm</strong>',
      ),
   )

   result, output = _check_hours( database, capsys )
   rows = _hour_rows( database, ZOOM )
   current = rows[ -1 ]

   assert result == 0
   assert 'Extended the attraction hours through ' in output
   assert current[ 'SCHEDULE_START_DATE' ] == HOURS_DAY.isoformat()
   assert current[ 'SCHEDULE_END_DATE' ] == SEASON_END
   assert current[ 'WEEKDAY_END_TIME' ] == '4:00 PM'
   assert current[ 'WEEKEND_HOLIDAY_END_TIME' ] == '5:30 PM'


def Test_CheckSchedules_TestLaterEnd_ExpectTrimmed(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ ZOOM ],
      [ ( ZOOM, '2026-07-29', '2026-12-31', '10:00 AM', '4:00 PM', '10:00 AM', '5:30 PM' ) ],
      [ ( ZOOM, DAILY, 0 ) ],
   )
   _install_page(
      monkeypatch,
      _hours_card(
         ZOOM,
         'Open Daily',
         '<strong>Weekdays: 10:00am - 4:00pm Weekends/Holidays: 10:00am - 5:30pm</strong>',
      ),
   )

   result, output = _check_hours( database, capsys )
   current = _hour_rows( database, ZOOM )[ -1 ]

   assert result == 0
   assert 'Trimmed the attraction hours through ' in output
   assert current[ 'SCHEDULE_START_DATE' ] == HOURS_DAY.isoformat()
   assert current[ 'SCHEDULE_END_DATE' ] == SEASON_END


def Test_CheckSchedules_TestWeekendSpan_ExpectStoredWeekdays(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ SPLASH ],
      [ ( SPLASH, '2026-07-29', SEASON_END, '10:00 AM', '4:00 PM', '11:00 AM', '6:00 PM' ) ],
      [ ( SPLASH, WEEKEND, 0 ) ],
   )
   _install_page(
      monkeypatch,
      _hours_card( SPLASH, 'Open Weekends', '<strong>11:00am - 5:00pm</strong>' ),
   )

   result, output = _check_hours( database, capsys )
   current = _hour_rows( database, SPLASH )[ -1 ]

   assert result == 0
   assert '10:00 AM to 4:00 PM on weekdays and 11:00 AM to 5:00 PM on weekends and holidays' in output
   assert current[ 'WEEKDAY_START_TIME' ] == '10:00 AM'
   assert current[ 'WEEKDAY_END_TIME' ] == '4:00 PM'
   assert current[ 'WEEKEND_HOLIDAY_START_TIME' ] == '11:00 AM'
   assert current[ 'WEEKEND_HOLIDAY_END_TIME' ] == '5:00 PM'


def Test_CheckSchedules_TestDuringZooHours_ExpectHeaderHours(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours( database, [ GREENHOUSE ], [], [ ( GREENHOUSE, DAILY, 0 ) ] )
   card = _hours_card( GREENHOUSE, 'Open Daily', '<strong>During Zoo Hours</strong>' )
   _install_page(
      monkeypatch,
      'Weekdays: 9:30am - 4:30pm Weekends: 9:30am - 6:00pm' + card,
   )

   result, output = _check_hours( database, capsys )
   rows = _hour_rows( database, GREENHOUSE )

   assert result == 0
   assert '9:30 AM to 4:30 PM on weekdays and 9:30 AM to 6:00 PM on weekends and holidays' in output
   assert len( rows ) == 1
   assert rows[ 0 ][ 'WEEKDAY_END_TIME' ] == '4:30 PM'
   assert rows[ 0 ][ 'WEEKEND_HOLIDAY_END_TIME' ] == '6:00 PM'


def Test_CheckSchedules_TestNoPublishedClock_ExpectNoWrite(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ ZOOM, SPLASH, 'Kangaroo Walk-Thru' ],
      [],
      [
         ( ZOOM, DAILY, 0 ),
         ( 'Kangaroo Walk-Thru', WEEKEND, 1 ),
      ],
   )
   _install_page(
      monkeypatch,
      _hours_card( ZOOM, 'Open Daily', '<strong>Weather Permitting</strong>' )
      + _hours_card( SPLASH, 'Closed for the Season', '<strong>10:30am - 6:00pm</strong>' )
      + _hours_card(
         'Kangaroo Walk-Thru',
         'Open Weekends & Holidays',
         '<strong>Times May Vary</strong>',
      ),
   )

   result, output = _check_hours( database, capsys )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert 'Set the attraction hours' not in output
   assert _hour_rows( database, ZOOM ) == []
   assert _hour_rows( database, SPLASH ) == []


def Test_CheckSchedules_TestTourDescription_ExpectWeekendHours(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   carousel = 'Conservation Carousel'
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ carousel ],
      [ ( carousel, '2026-07-29', SEASON_END, '9:30 AM', '6:00 PM', '9:30 AM', '7:00 PM' ) ],
      [ ( carousel, WEEKEND, 1 ) ],
   )
   _install_page(
      monkeypatch,
      _hours_card( carousel, 'Open Weekends & Holidays', '<strong>Weather Permitting</strong>' ),
   )

   def tour_description( cls: type, href: str ) -> str:
      return '<strong>10:00am - 4:30pm</strong><strong>Weather Permitting</strong>'

   monkeypatch.setattr(
      AttractionHoursReader,
      'tour_description',
      classmethod( tour_description ),
   )

   result, output = _check_hours( database, capsys )
   current = _hour_rows( database, carousel )[ -1 ]

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert '9:30 AM to 6:00 PM on weekdays and 10:00 AM to 4:30 PM on weekends and holidays' in output
   assert current[ 'WEEKDAY_START_TIME' ] == '9:30 AM'
   assert current[ 'WEEKDAY_END_TIME' ] == '6:00 PM'
   assert current[ 'WEEKEND_HOLIDAY_START_TIME' ] == '10:00 AM'
   assert current[ 'WEEKEND_HOLIDAY_END_TIME' ] == '4:30 PM'


def Test_CheckSchedules_TestShorterZooHours_ExpectEndBeforeThatDay(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours( database, [ ZOOM ], [], [ ( ZOOM, DAILY, 0 ) ] )
   connection = sqlite3.connect( database )
   connection.execute(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            ) VALUES ( '2026-10-10', '08:30', '11:00', '14:00', '15:00' )
      """
   )
   connection.commit()
   connection.close()
   _install_page(
      monkeypatch,
      _hours_card( ZOOM, 'Open Daily', '<strong>10:00am - 4:30pm</strong>' ),
   )

   result, output = _check_hours( database, capsys )
   current = _hour_rows( database, ZOOM )[ -1 ]

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert 'through October 9' in output
   assert current[ 'SCHEDULE_END_DATE' ] == '2026-10-09'
   assert current[ 'WEEKDAY_END_TIME' ] == '4:30 PM'


def Test_CheckSchedules_TestScheduleAndHours_ExpectOneFix(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours( database, [ ZOOM ], [], [ ( ZOOM, DAILY, 0 ) ] )
   connection = sqlite3.connect( database )
   connection.execute(
      """   UPDATE AttractionOpeningSchedule
            SET SCHEDULE_END_DATE = '2026-09-07'
      """
   )
   connection.commit()
   connection.close()
   _install_page(
      monkeypatch,
      _hours_card( ZOOM, 'Open Daily', '<strong>10:00am - 4:30pm</strong>' ),
   )

   result, output = _check_hours( database, capsys )
   day_line = next(
      line for line in output.splitlines() if '10:00 AM to 4:30 PM' in line
   )

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert 'Extended the schedule through October 31, 2026.' in output
   assert CheckReport.text( 'format.bulletItem' ) in day_line
   assert 'from 10:00 AM to 4:30 PM' in day_line
   assert 'Set the attraction hours' not in output


def Test_CheckSchedules_TestChristmasZooHours_ExpectHoursResumeAfterChristmas(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours( database, [ ZOOM ], [], [ ( ZOOM, DAILY, 0 ) ] )
   _prepare_christmas( database )
   _install_page(
      monkeypatch,
      _hours_card( ZOOM, 'Open Daily', '<strong>10:00am - 4:30pm</strong>' ),
   )
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, date( 2026, 11, 16 ) )
   output = capsys.readouterr().out
   rows = _hour_rows( database, ZOOM )

   assert result == 0
   assert CheckReport.fixed_count == 2
   assert len( rows ) == 2
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == '2026-11-16'
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == '2026-12-24'
   assert rows[ 1 ][ 'SCHEDULE_START_DATE' ] == '2026-12-26'
   assert rows[ 1 ][ 'SCHEDULE_END_DATE' ] == '2026-12-31'
   assert output.count( ZOOM ) == 1
   assert output.count( 'Set the attraction hours from' ) == 1
   bullet = CheckReport.text( 'format.bulletItem' )
   assert 'Set the attraction hours from 10:00 AM to 4:30 PM:' in output
   assert bullet + 'through December 24, 2026.' in output
   assert bullet + 'from December 26, 2026 through December 31, 2026.' in output


def Test_CheckSchedules_TestChristmasInsideStoredHours_ExpectSplitAroundChristmas(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_hours(
      database,
      [ ZOOM ],
      [ ( ZOOM, '2026-07-29', '2026-12-31', '10:00 AM', '4:30 PM', '10:00 AM', '4:30 PM' ) ],
      [ ( ZOOM, DAILY, 0 ) ],
   )
   _prepare_christmas( database )
   _install_page(
      monkeypatch,
      _hours_card( ZOOM, 'Open Daily', '<strong>10:00am - 4:30pm</strong>' ),
   )
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, date( 2026, 11, 16 ) )
   output = capsys.readouterr().out
   rows = _hour_rows( database, ZOOM )

   assert result == 0
   assert CheckReport.fixed_count == 2
   assert len( rows ) == 2
   assert rows[ 0 ][ 'SCHEDULE_START_DATE' ] == '2026-11-16'
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == '2026-12-24'
   assert rows[ 1 ][ 'SCHEDULE_START_DATE' ] == '2026-12-26'
   assert rows[ 1 ][ 'SCHEDULE_END_DATE' ] == '2026-12-31'
   assert 'through December 24' in output
   assert 'from December 26' in output
