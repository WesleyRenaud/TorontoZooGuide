from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_email_renderer import CheckEmailRenderer
from tools.checks.check_report import CheckReport
from tools.checks.check_report_parser import CheckReportParser
from tools.checks.guardians_talk_comparison import GuardiansTalkComparison
from tools.checks.guardians_talk_detail_image import GuardiansTalkDetailImage
from tools.checks.guardians_talk_listing import GuardiansTalkListing
from tools.checks.guardians_talk_schedule_checker import GuardiansTalkScheduleChecker as CHECKER
from tools.checks.website_page import WebsitePage


TALK = 'Snow Leopard'
LOCATION = 'Eurasia Wilds'
WEBSITE_LOCATION = 'Eurasia'
CLOCK = '1:00 PM'
WEBSITE_CLOCK = '1:00pm'
OTHER_CLOCK = '11:00 AM'
WEBSITE_OTHER_CLOCK = '11:00am'
TODAY = date( 2026, 11, 1 )
THURSDAY = date( 2026, 11, 5 )
NEXT_THURSDAY = THURSDAY + timedelta( days=7 )
AFTER_WINDOW = NEXT_THURSDAY + timedelta( days=7 )
SCHEMA = """
CREATE TABLE MeetTheGuardiansTalk (
   NAME             TEXT NOT NULL,
   LOCATION         TEXT NOT NULL,
   ENCLOSURE_NAME   TEXT,
   X_COORD          FLOAT NOT NULL DEFAULT 0,
   Y_COORD          FLOAT NOT NULL DEFAULT 0,
   MAXIMUM_DURATION INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY ( NAME, LOCATION, ENCLOSURE_NAME )
);

CREATE TABLE GuardiansTalkSchedule (
   TALK_NAME            TEXT NOT NULL,
   LOCATION             TEXT NOT NULL,
   ENCLOSURE_NAME       TEXT,
   SCHEDULE_START_DATE  DATE NOT NULL,
   SCHEDULE_END_DATE    DATE,
   MONDAY               BOOL NOT NULL DEFAULT 0,
   TUESDAY              BOOL NOT NULL DEFAULT 0,
   WEDNESDAY            BOOL NOT NULL DEFAULT 0,
   THURSDAY             BOOL NOT NULL DEFAULT 0,
   FRIDAY               BOOL NOT NULL DEFAULT 0,
   SATURDAY             BOOL NOT NULL DEFAULT 0,
   SUNDAY               BOOL NOT NULL DEFAULT 0,
   TALK_TIME            TEXT NOT NULL,
   SCHEDULE_MESSAGE     TEXT,
   PRIMARY KEY (
      TALK_NAME,
      LOCATION,
      ENCLOSURE_NAME,
      TALK_TIME,
      SCHEDULE_START_DATE
   )
);

CREATE TABLE GuardiansTalkAnimal (
   TALK_NAME       TEXT NOT NULL,
   LOCATION        TEXT NOT NULL,
   ENCLOSURE_NAME  TEXT,
   SPECIES         TEXT NOT NULL,
   EXHIBIT         TEXT NOT NULL
);

CREATE TABLE GuardiansTalkCancellation (
   TALK_NAME          TEXT NOT NULL,
   LOCATION           TEXT NOT NULL,
   ENCLOSURE_NAME     TEXT,
   CANCELLATION_DATE  DATE NOT NULL,
   TALK_TIME          TEXT NOT NULL,
   PRIMARY KEY (
      TALK_NAME,
      LOCATION,
      ENCLOSURE_NAME,
      CANCELLATION_DATE,
      TALK_TIME
   )
);
"""




def _weekday_values( weekdays: set[ int ] ) -> tuple[ int, int, int, int, int, int, int ]:
   flags = [ 1 if index in weekdays else 0 for index in range( 7 ) ]
   return flags[ 0 ], flags[ 1 ], flags[ 2 ], flags[ 3 ], flags[ 4 ], flags[ 5 ], flags[ 6 ]


def _catalog_row(
      row: tuple[ str, str ] | tuple[ str, str, str | None ],
      ) -> tuple[ str, str, str | None ]:
   if len( row ) == 2:
      return row[ 0 ], row[ 1 ], None

   return row


def _schedule_row(
      row: tuple[ str, str, str, str | None, str, set[ int ] ]
      | tuple[ str, str, str | None, str, str | None, str, set[ int ] ],
      ) -> tuple[ str, str, str | None, str, str | None, str, set[ int ] ]:
   if len( row ) == 6:
      return row[ 0 ], row[ 1 ], None, row[ 2 ], row[ 3 ], row[ 4 ], row[ 5 ]

   return row


def _write_database(
      path: Path,
      catalog: list[ tuple[ str, str ] | tuple[ str, str, str | None ] ],
      schedules: list[
         tuple[ str, str, str, str | None, str, set[ int ] ]
         | tuple[ str, str, str | None, str, str | None, str, set[ int ] ]
      ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      """   INSERT INTO MeetTheGuardiansTalk (
               NAME,
               LOCATION,
               ENCLOSURE_NAME
            ) VALUES ( ?, ?, ? )
      """,
      [ _catalog_row( row ) for row in catalog ],
   )

   for row in schedules:
      name, location, enclosure, start, end, talk_time, weekdays = _schedule_row( row )
      connection.execute(
         """   INSERT INTO GuardiansTalkSchedule (
                  TALK_NAME,
                  LOCATION,
                  ENCLOSURE_NAME,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  TALK_TIME
               ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
         """,
         (
            name,
            location,
            enclosure,
            start,
            end,
            *_weekday_values( weekdays ),
            talk_time,
         ),
      )

   connection.commit()
   connection.close()


def _page( days: list[ tuple[ date, list[ tuple[ str, str, str ] ] ] ] ) -> str:
   parts = [ '<div class="programme-schedule">' ]

   for scheduled_date, talks in days:
      weekday = scheduled_date.strftime( '%A' )
      month = scheduled_date.strftime( '%B' )
      parts.append( f'<div class="cstrong">{ weekday }, { month } { scheduled_date.day }</div>' )

      for talk_time, name, location in talks:
         parts.append(
            '<div class="aname">'
            f'{ name }</div><div class="talklocation">{ location }</div>{ talk_time }'
         )

   parts.append( '</div>' )
   return ''.join( parts )


def _install_page(
      monkeypatch: pytest.MonkeyPatch,
      page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _schedule_end( path: Path, name: str ) -> str:
   connection = sqlite3.connect( path )
   row = connection.execute(
      """   SELECT SCHEDULE_END_DATE
            FROM GuardiansTalkSchedule
            WHERE TALK_NAME = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()
   return row[ 0 ]


def _cancellations( path: Path, name: str ) -> list[ str ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      """   SELECT CANCELLATION_DATE
            FROM GuardiansTalkCancellation
            WHERE TALK_NAME = ?
            ORDER BY CANCELLATION_DATE
      """,
      ( name, ),
   ).fetchall()
   connection.close()
   return [ row[ 0 ] for row in rows ]


def _schedule_count( path: Path, name: str ) -> int:
   connection = sqlite3.connect( path )
   row = connection.execute(
      """   SELECT COUNT( * )
            FROM GuardiansTalkSchedule
            WHERE TALK_NAME = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()
   return row[ 0 ]


def _check( database: Path, capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = CHECKER.check_schedules( database, TODAY )
   return result, capsys.readouterr().out


def _email( output: str, issues: int ) -> str:
   label = CheckReportParser.format_error_count( issues )
   counts = CheckReportParser.format_counts( talks=issues )
   body = (
      f'{ output }\n'
      f'{ counts }\n\n'
      f'{ label }\n'
   )
   return CheckEmailRenderer.render_html( body, 1 if issues else 0 )


def Test_ParseHeading_TestJanuaryAfterDecember_ExpectNextYear() -> None:
   today = date( 2026, 12, 28 )

   parsed = GuardiansTalkComparison.parse_heading( 'Friday, January 2', today )

   assert parsed == date( today.year + 1, 1, 2 )


def Test_ParseHeading_TestDecemberBeforeJanuary_ExpectThisYear() -> None:
   today = date( 2027, 1, 2 )

   parsed = GuardiansTalkComparison.parse_heading( 'Wednesday, December 30', today )

   assert parsed == date( today.year, 12, 30 )


def Test_CheckSchedules_TestClosedToday_ExpectTodayFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   tomorrow = TODAY + timedelta( days=1 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ), ( 'Domestic Goat', LOCATION ) ],
      [
         (
            'Domestic Goat',
            LOCATION,
            TODAY.isoformat(),
            tomorrow.isoformat(),
            CLOCK,
            { TODAY.weekday() },
         ),
         (
            TALK,
            LOCATION,
            tomorrow.isoformat(),
            ( tomorrow + timedelta( days=1 ) ).isoformat(),
            CLOCK,
            { tomorrow.weekday() },
         ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( TODAY, [ ( WEBSITE_CLOCK, 'West Caucasian tur', WEBSITE_LOCATION ) ] ),
         ( tomorrow, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
      ] ),
   )

   result, output = _check( database, capsys )

   assert result == 1
   assert 'West Caucasian tur' in output
   assert 'Domestic Goat' in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert _schedule_count( database, 'Domestic Goat' ) == 0
   assert CheckReport.text( 'checks.websiteDatesCompared' ) + TODAY.isoformat() in output


def Test_CheckSchedules_TestOtherEnclosureSchedule_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   friday = date( 2026, 11, 6 )
   saturday = friday + timedelta( days=1 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION, 'Indoor' ) ],
      [
         (
            TALK,
            LOCATION,
            None,
            friday.isoformat(),
            ( saturday + timedelta( days=1 ) ).isoformat(),
            CLOCK,
            { friday.weekday() },
         ),
         (
            TALK,
            LOCATION,
            'Indoor',
            saturday.isoformat(),
            ( saturday + timedelta( days=1 ) ).isoformat(),
            CLOCK,
            { saturday.weekday() },
         ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( friday, [] ),
         ( saturday, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
      ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output


def Test_CheckSchedules_TestAppTalkAfterWindow_ExpectScheduleRemoved(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( 'Amur Tiger', LOCATION ), ( TALK, LOCATION ) ],
      [
         (
            'Amur Tiger',
            LOCATION,
            TODAY.isoformat(),
            ( TODAY + timedelta( days=1 ) ).isoformat(),
            '11:00 AM',
            { TODAY.weekday() },
         ),
         (
            TALK,
            LOCATION,
            THURSDAY.isoformat(),
            AFTER_WINDOW.isoformat(),
            CLOCK,
            { THURSDAY.weekday() },
         ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( TODAY, [ ( '11:00am', 'Amur tiger', WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   talk = GuardiansTalkListing( name=TALK, location=LOCATION )
   assert result == 0
   assert f'  { GuardiansTalkComparison.label( talk ) }' in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert _schedule_count( database, TALK ) == 0
   assert 'Amur Tiger' not in output
   assert THURSDAY.isoformat() not in output


def Test_CheckSchedules_TestAppOnlyInsideWindow_ExpectScheduleRemoved(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         THURSDAY.isoformat(),
         ( THURSDAY + timedelta( days=1 ) ).isoformat(),
         CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page( monkeypatch, _page( [ ( THURSDAY, [] ) ] ) )
   connection = sqlite3.connect( database )
   connection.execute(
      """   INSERT INTO GuardiansTalkAnimal (
               TALK_NAME,
               LOCATION,
               ENCLOSURE_NAME,
               SPECIES,
               EXHIBIT )
            VALUES ( ?, ?, NULL, ?, ? )
      """,
      ( TALK, LOCATION, TALK, LOCATION ),
   )
   connection.commit()
   connection.close()

   result, output = _check( database, capsys )

   talk = GuardiansTalkListing( name=TALK, location=LOCATION )
   photo = AnimalDetailImage.source( LOCATION, TALK )
   assert result == 0
   assert f'  { GuardiansTalkComparison.label( talk ) }' in output
   assert photo in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert _schedule_count( database, TALK ) == 0
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) in output
   html = _email( output, result )
   assert 'Guardians Talks' in html
   assert TALK in html
   assert CheckEmailRenderer.image_src( photo ) in html
   assert CheckReport.text( 'checks.scheduledInAppOnly' ) in html
   assert CheckReport.text( 'checks.removedSchedule' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestWebsiteOnly_ExpectWebsiteViolation(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( TALK, LOCATION ) ], [] )
   _install_page(
      monkeypatch,
      _page( [ ( THURSDAY, [ ( WEBSITE_CLOCK, 'West Caucasian tur', WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   website_talk = GuardiansTalkListing( name='West Caucasian tur', location=WEBSITE_LOCATION )
   assert result == 1
   assert f'  { GuardiansTalkComparison.label( website_talk ) }' in output
   assert f'  { GuardiansTalkComparison.label( GuardiansTalkListing( name=TALK, location=LOCATION ) ) }' not in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 1 ) in output
   html = _email( output, result )
   assert 'West Caucasian tur' in html
   assert CheckReport.text( 'checks.scheduledOnWebsiteOnly' ) in html
   assert TALK not in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestCatalogTalkWithoutSchedule_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( TALK, LOCATION ) ], [] )
   _install_page(
      monkeypatch,
      _page( [ ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert f'  { GuardiansTalkComparison.label( GuardiansTalkListing( name=TALK, location=LOCATION ) ) }' in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 5, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert _schedule_count( database, TALK ) == 1
   assert _schedule_end( database, TALK ) == THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestScheduleEndedBeforeWindow_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   ended = date( 2026, 10, 29 )
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         ended.isoformat(),
         ( ended + timedelta( days=1 ) ).isoformat(),
         OTHER_CLOCK,
         { ended.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 5, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert _schedule_count( database, TALK ) == 1
   assert _schedule_end( database, TALK ) == THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestDifferentTime_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         THURSDAY.isoformat(),
         ( THURSDAY + timedelta( days=1 ) ).isoformat(),
         OTHER_CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 5, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert _schedule_end( database, TALK ) == THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestWebsiteWindowLonger_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         THURSDAY.isoformat(),
         ( THURSDAY + timedelta( days=1 ) ).isoformat(),
         CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
         ( NEXT_THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
      ] ),
   )

   result, output = _check( database, capsys )

   photo = GuardiansTalkDetailImage.source( LOCATION, TALK )
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert photo in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 12, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert CheckReport.text( 'checks.websiteDatesNotInApp' ) not in output
   assert CheckReport.text( 'checks.appDatesNotOnWebsite' ) not in output
   assert _schedule_end( database, TALK ) == NEXT_THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckEmailRenderer.image_src( photo ) in html
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestAppWindowLonger_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         THURSDAY.isoformat(),
         ( AFTER_WINDOW + timedelta( days=1 ) ).isoformat(),
         CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
         ( NEXT_THURSDAY, [] ),
      ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 5, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert AFTER_WINDOW.isoformat() not in output
   assert CheckReport.text( 'checks.appDatesNotOnWebsite' ) not in output
   assert CheckReport.text( 'checks.websiteDatesNotInApp' ) not in output
   assert _schedule_end( database, TALK ) == THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html


def Test_CheckSchedules_TestAppDateBetweenWebsiteDates_ExpectNoViolation(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         THURSDAY.isoformat(),
         AFTER_WINDOW.isoformat(),
         CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
         ( NEXT_THURSDAY, [] ),
         ( AFTER_WINDOW, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ),
      ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) not in output
   assert _schedule_end( database, TALK ) == AFTER_WINDOW.isoformat()
   assert _cancellations( database, TALK ) == []


def Test_CheckSchedules_TestAppWindowPastWebsite_ExpectWindowFixed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TALK, LOCATION ) ],
      [ (
         TALK,
         LOCATION,
         TODAY.isoformat(),
         ( AFTER_WINDOW + timedelta( days=1 ) ).isoformat(),
         CLOCK,
         { THURSDAY.weekday() },
      ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( THURSDAY, [ ( WEBSITE_CLOCK, TALK, WEBSITE_LOCATION ) ] ) ] ),
   )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 0 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 5, 2026 through November 5, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }1:00 PM Thu' in output
   assert AFTER_WINDOW.isoformat() not in output
   assert _schedule_end( database, TALK ) == THURSDAY.isoformat()
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.websiteDatesCompared' ) not in html
