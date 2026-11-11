from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from api.app_string_provider import AppStringProvider
from tools.checks.booking_calendar import BookingCalendar
from tools.checks.check_email_renderer import CheckEmailRenderer
from tools.checks.check_report import CheckReport
from tools.checks.check_report_parser import CheckReportParser
from tools.checks.website_page import WebsitePage
from tools.checks.wild_encounter_comparison import WildEncounterComparison
from tools.checks.wild_encounter_detail_image import WildEncounterDetailImage
from tools.checks.wild_encounter_schedule_checker import WildEncounterScheduleChecker as CHECKER


GIRAFFE = 'Giraffe'
GIRAFFE_LINK = 'https://example.test/giraffe'
GIRAFFE_TOUR = '42'
KANGAROO = 'Kangaroo'
KANGAROO_LINK = 'https://example.test/kangaroo'
SNOW_LEOPARD = 'Guardians of Snow Leopards'
SNOW_LEOPARD_WEBSITE = 'Snow Leopard'
SNOW_LEOPARD_LINK = 'https://example.test/snow'
TODAY = date( 2026, 11, 1 )
SCHEDULE_START = TODAY
SCHEDULE_END = date( 2026, 11, 5 )
CLOCK = '11:00 AM'
REGION = 'Africa'
WEBSITE_CLOCK = '11:00'
OTHER_CLOCK = '2:00'
SCHEMA = """
CREATE TABLE WildEncounter (
   NAME              TEXT    NOT NULL,
   MEETING_SPOT      TEXT    NOT NULL,
   LINK              TEXT    NOT NULL,
   MAXIMUM_DURATION  INTEGER NOT NULL,
   PRIMARY KEY ( NAME )
);

CREATE TABLE WildEncounterMeetingSpot (
   NAME      TEXT NOT NULL,
   X_COORD   FLOAT,
   Y_COORD   FLOAT,
   REGION    TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);

CREATE TABLE WildEncounterSchedule (
   WILD_ENCOUNTER       TEXT NOT NULL,
   SCHEDULE_START_DATE  DATE NOT NULL,
   SCHEDULE_END_DATE    DATE,
   MONDAY               BOOL NOT NULL DEFAULT 0,
   TUESDAY              BOOL NOT NULL DEFAULT 0,
   WEDNESDAY            BOOL NOT NULL DEFAULT 0,
   THURSDAY             BOOL NOT NULL DEFAULT 0,
   FRIDAY               BOOL NOT NULL DEFAULT 0,
   SATURDAY             BOOL NOT NULL DEFAULT 0,
   SUNDAY               BOOL NOT NULL DEFAULT 0,
   ENCOUNTER_TIME       TEXT NOT NULL,
   SCHEDULE_MESSAGE     TEXT,
   PRIMARY KEY ( WILD_ENCOUNTER, ENCOUNTER_TIME, SCHEDULE_START_DATE )
);
"""




def _write_database(
      path: Path,
      catalog: list[ tuple[ str, str ] ],
      schedules: list[ tuple[ str, str, str, str ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.execute(
      """   INSERT INTO WildEncounterMeetingSpot (
               NAME,
               X_COORD,
               Y_COORD,
               REGION )
            VALUES ( 'Spot', 0, 0, ? )
      """,
      ( REGION, ),
   )
   connection.executemany(
      """   INSERT INTO WildEncounter (
               NAME,
               MEETING_SPOT,
               LINK,
               MAXIMUM_DURATION )
            VALUES ( ?, 'Spot', ?, 30 )
      """,
      catalog )
   connection.executemany(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               ENCOUNTER_TIME,
               SCHEDULE_MESSAGE )
            VALUES ( ?, ?, ?, 1, 1, 1, 1, 1, 1, 1, ?, '' )
      """,
      schedules )
   connection.commit()
   connection.close()


def _encounter_card( name: str, image: str ) -> str:
   return (
      f'<a class="col3" href="/tickets/wepenguin">'
      f'<img alt="" src="{ image }" />'
      f'<div class="col3title">{ name }</div>'
      f'</a>'
   )


def _schedule_page( rows: list[ tuple[ str, str ] ] ) -> str:
   header = (
      '<tr><th>Time</th><th>Sunday</th><th>Monday</th><th>Tuesday</th>'
      '<th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr>'
   )
   body = []

   for encounter_time, name in rows:
      cells = ''.join( f'<td>{ name }</td>' for _day in range( 7 ) )
      body.append( f'<tr><td>{ encounter_time }</td>{ cells }</tr>' )

   return f'<table>{ header }{ "".join( body ) }</table>'


def _booking_page( tour_id: str ) -> str:
   return f'<div class="hb-tour-wrapper" tour-id="{ tour_id }"></div>'


def _enabled_dates( days: list[ date ] ) -> dict[ str, object ]:
   return {
      'data': {
         'enabledDates': [
            {
               'year': TODAY.year % 100,
               'months': [
                  {
                     'month': TODAY.month,
                     'days': [ item.day for item in days ],
                  },
               ],
            },
         ],
      },
   }


def _matched_dates() -> list[ date ]:
   last = SCHEDULE_END - timedelta( days=1 )
   return [
      TODAY + timedelta( days=offset )
      for offset in range( ( last - TODAY ).days + 1 )
   ]


def _install_web(
      monkeypatch: pytest.MonkeyPatch,
      pages: dict[ str, str ],
      calendars: dict[ str, dict[ str, object ] ] ) -> None:
   def fetch_text( url: str ) -> str:
      return pages[ url ]

   def post_json( url: str, payload: dict[ str, object ] ) -> dict[ str, object ]:
      if url != BookingCalendar.GRAPHQL_URL:
         raise RuntimeError( url )

      variables = payload[ 'variables' ]

      if not isinstance( variables, dict ):
         raise RuntimeError( 'Missing booking variables.' )

      return calendars[ str( variables[ 'bookingType' ] ) ]

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )
   monkeypatch.setattr( BookingCalendar, 'post_json', post_json )


def _email( output: str, issues: int ) -> str:
   label = CheckReportParser.format_error_count( issues )
   counts = CheckReportParser.format_counts( encounters=issues )
   body = (
      f'{ output }\n'
      f'{ counts }\n\n'
      f'{ label }\n'
   )
   return CheckEmailRenderer.render_html( body, 1 if issues else 0 )


def _giraffe_database( path: Path, encounter_time: str ) -> None:
   _write_database(
      path,
      [ ( GIRAFFE, GIRAFFE_LINK ) ],
      [ (
         GIRAFFE,
         SCHEDULE_START.isoformat(),
         SCHEDULE_END.isoformat(),
         encounter_time,
      ) ] )


def _schedule_end( path: Path, name: str ) -> str:
   connection = sqlite3.connect( path )
   row = connection.execute(
      """   SELECT SCHEDULE_END_DATE
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()
   return row[ 0 ]


def _giraffe_pages( website_time: str ) -> dict[ str, str ]:
   return {
      WebsitePage.url( WildEncounterComparison.PAGE ): _schedule_page( [ ( website_time, GIRAFFE ) ] ),
      GIRAFFE_LINK: _booking_page( GIRAFFE_TOUR ),
   }


def _encounter_label( name: str ) -> str:
   return AppStringProvider.format(
      'format.middleDotPair',
      first=name,
      second=REGION,
   )


def _schedule_count( path: Path, name: str ) -> int:
   connection = sqlite3.connect( path )
   row = connection.execute(
      """   SELECT COUNT( * )
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()
   return row[ 0 ]


def Test_CheckSchedules_TestAppOnlyEncounter_ExpectScheduleRemoved(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( GIRAFFE, GIRAFFE_LINK ), ( 'Masai Giraffe', KANGAROO_LINK ) ],
      [
         (
            GIRAFFE,
            SCHEDULE_START.isoformat(),
            SCHEDULE_END.isoformat(),
            CLOCK,
         ),
         (
            'Masai Giraffe',
            SCHEDULE_START.isoformat(),
            SCHEDULE_END.isoformat(),
            CLOCK,
         ),
      ] )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 1 ) in output
   photo = WildEncounterDetailImage.source( 'Masai Giraffe' )
   assert f'  { _encounter_label( "Masai Giraffe" ) }' in output
   assert photo in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert _schedule_count( database, 'Masai Giraffe' ) == 0
   assert _schedule_count( database, GIRAFFE ) == 1
   assert f'  { _encounter_label( GIRAFFE ) }' not in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   html = _email( output, result )
   assert 'Masai Giraffe' in html
   assert CheckEmailRenderer.image_src( photo ) in html
   assert CheckReport.text( 'checks.scheduledInAppOnly' ) in html
   assert CheckReport.text( 'checks.removedSchedule' ) in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html
   assert f'>{ GIRAFFE }<' not in html


def Test_CheckSchedules_TestFutureEncounterNotOnWebsite_ExpectScheduleRemoved(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( GIRAFFE, GIRAFFE_LINK ), ( KANGAROO, KANGAROO_LINK ) ],
      [
         (
            GIRAFFE,
            SCHEDULE_START.isoformat(),
            SCHEDULE_END.isoformat(),
            CLOCK,
         ),
         (
            KANGAROO,
            SCHEDULE_END.isoformat(),
            ( SCHEDULE_END + timedelta( days=7 ) ).isoformat(),
            CLOCK,
         ),
      ] )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 1 ) in output
   assert f'  { _encounter_label( KANGAROO ) }' in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert _schedule_count( database, KANGAROO ) == 0
   assert _schedule_count( database, GIRAFFE ) == 1
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output


def Test_CheckSchedules_TestScheduleEndedToday_ExpectScheduleRemoved(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( GIRAFFE, GIRAFFE_LINK ), ( KANGAROO, KANGAROO_LINK ) ],
      [
         (
            GIRAFFE,
            SCHEDULE_START.isoformat(),
            SCHEDULE_END.isoformat(),
            CLOCK,
         ),
         (
            KANGAROO,
            TODAY.isoformat(),
            ( TODAY + timedelta( days=1 ) ).isoformat(),
            CLOCK,
         ),
      ] )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert f'  { _encounter_label( KANGAROO ) }' in output
   assert CheckReport.text( 'checks.removedSchedule' ) in output
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 1 ) in output
   assert _schedule_count( database, KANGAROO ) == 0
   assert _schedule_count( database, GIRAFFE ) == 1


def Test_CheckSchedules_TestUnscheduledEncounter_ExpectWindowFixed(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( GIRAFFE, GIRAFFE_LINK ),
         ( SNOW_LEOPARD, SNOW_LEOPARD_LINK ),
      ],
      [ (
         GIRAFFE,
         SCHEDULE_START.isoformat(),
         SCHEDULE_END.isoformat(),
         CLOCK,
      ) ] )
   pages = _giraffe_pages( WEBSITE_CLOCK )
   penguin_image = '/!/img/pg/wildencounters/penguin.webp'
   pages[ WebsitePage.url( WildEncounterComparison.PAGE ) ] = (
      _schedule_page( [
         ( WEBSITE_CLOCK, GIRAFFE ),
         ( WEBSITE_CLOCK, SNOW_LEOPARD_WEBSITE ),
         ( WEBSITE_CLOCK, 'Penguin Splash' ),
      ] )
      + _encounter_card( 'Penguin Splash', penguin_image )
   )
   pages[ SNOW_LEOPARD_LINK ] = _booking_page( '99' )
   _install_web(
      monkeypatch,
      pages,
      {
         GIRAFFE_TOUR: _enabled_dates( _matched_dates() ),
         '99': _enabled_dates( _matched_dates() ),
      } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 1
   penguin_photo = WebsitePage.absolute_url( penguin_image )
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 1 ) in output
   assert CheckReport.join_lines( [
      CheckReport.text( 'checks.categoryItem' ) + 'Penguin Splash',
      CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + penguin_photo ),
   ] ) in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert f'  { _encounter_label( SNOW_LEOPARD ) }' in output
   assert f'  { SNOW_LEOPARD_WEBSITE }' not in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 2, 2026 through November 4, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }11:00 AM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in output
   html = _email( output, result )
   assert SNOW_LEOPARD in html
   assert penguin_photo in html
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html


def Test_CheckSchedules_TestDifferentTime_ExpectWindowFixed(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( OTHER_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert f'  { _encounter_label( GIRAFFE ) }' in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 2, 2026 through November 4, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }2:00 PM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in output
   assert _schedule_end( database, GIRAFFE ) == '2026-11-05'
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html


def Test_CheckSchedules_TestBookableWindowLonger_ExpectWindowViolation(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   matched = _matched_dates()
   extra_start = matched[ -1 ] + timedelta( days=1 )
   extra_end = extra_start + timedelta( days=1 )
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( [ *matched, extra_start, extra_end ] ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert f'  { _encounter_label( GIRAFFE ) }' in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 2, 2026 through November 6, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }11:00 AM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in output
   assert CheckReport.text( 'checks.bookableDatesNotInApp' ) not in output
   assert _schedule_end( database, GIRAFFE ) == '2026-11-07'
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html


def Test_CheckSchedules_TestAppWindowLonger_ExpectWindowViolation(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   matched = _matched_dates()
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( [ matched[ 1 ] ] ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert f'  { _encounter_label( GIRAFFE ) }' in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 2, 2026 through November 2, 2026.' in output
   assert f'{ CheckReport.text( "format.bulletItem" ) }11:00 AM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in output
   assert CheckReport.text( 'checks.appDatesNotBookable' ) not in output
   assert _schedule_end( database, GIRAFFE ) == '2026-11-03'
   html = _email( output, result )
   assert CheckReport.text( 'checks.setScheduleFrom' ) in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html


def Test_CheckSchedules_TestMatchingWindow_ExpectNoViolations(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.scheduledInAppOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   html = _email( output, result )
   assert CheckReport.text( 'checks.status.noneDetected' ) in html
   assert CheckReport.text( 'checks.status.websiteMatches' ) in html
   assert GIRAFFE not in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html


def Test_CheckSchedules_TestUnscheduledWithImage_ExpectPhotoAndSchedule(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   name = 'Masai Giraffe'
   link = 'https://example.test/masai'
   _write_database( database, [ ( name, link ) ], [] )
   pages = {
      WebsitePage.url( WildEncounterComparison.PAGE ): _schedule_page( [ ( WEBSITE_CLOCK, name ) ] ),
      link: _booking_page( GIRAFFE_TOUR ),
   }
   _install_web(
      monkeypatch,
      pages,
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) },
   )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   photo = WildEncounterDetailImage.source( name )
   assert result == 0
   assert photo in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert _schedule_end( database, name ) == '2026-11-05'
   html = _email( output, result )
   assert CheckEmailRenderer.image_src( photo ) in html


def Test_CheckSchedules_TestTodayNotBookable_ExpectWindowKept(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   bookable = [ day for day in _matched_dates() if day != TODAY ]
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( bookable ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) not in output
   assert _schedule_count( database, GIRAFFE ) == 1
   assert _schedule_end( database, GIRAFFE ) == SCHEDULE_END.isoformat()


def Test_CheckSchedules_TestLaterDayStillDiffers_ExpectWebsiteWindow(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   bookable = [ day for day in _matched_dates() if day != TODAY ]
   later = bookable[ -1 ] + timedelta( days=2 )
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( [ *bookable, later ] ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert CheckReport.text( 'checks.setScheduleFrom' ) in output
   assert 'November 2, 2026 through November 6, 2026.' in output
   assert _schedule_end( database, GIRAFFE ) == '2026-11-07'
