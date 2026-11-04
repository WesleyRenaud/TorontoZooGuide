from __future__ import annotations

from datetime import date
from datetime import timedelta
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
import sqlite3
import types

import pytest

import tools.emailCheckSummary as email_summary


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

CREATE TABLE GuardiansTalkCancellation (
   TALK_NAME          TEXT NOT NULL,
   LOCATION           TEXT NOT NULL,
   ENCLOSURE_NAME     TEXT,
   CANCELLATION_DATE  DATE NOT NULL,
   TALK_TIME          TEXT NOT NULL
);
"""


def _load_checker() -> types.ModuleType:
   path = Path( __file__ ).resolve().parents[ 2 ] / 'tools' / 'guardiansTalkScheduleCheck.py'
   spec = spec_from_file_location( 'guardians_talk_schedule_check', path )

   if spec == None or spec.loader == None:
      raise RuntimeError( 'Could not load the schedule check.' )

   module = module_from_spec( spec )
   spec.loader.exec_module( module )
   return module


CHECKER = _load_checker()


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

   monkeypatch.setattr( CHECKER, 'fetch_text', fetch_text )


def _check( database: Path, capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = CHECKER.check_schedules( database, TODAY )
   return result, capsys.readouterr().out


def _email( output: str, issues: int ) -> str:
   label = '1 error' if issues == 1 else f'{ issues } errors'
   body = (
      f'{ output }\n'
      f'0 for encounters, { issues } for Guardians Talks, 0 for animals, '
      '0 for attractions, 0 for restaurants, 0 for gift shops, '
      '0 for drinking fountains, '
      '0 for the attraction list, 0 for the restaurant list, '
      '0 for the gift shop list, 0 for zoo hours\n\n'
      f'{ label }\n'
   )
   return email_summary.render_html( body, 1 if issues else 0 )


def Test_ParseHeading_TestJanuaryAfterDecember_ExpectNextYear() -> None:
   today = date( 2026, 12, 28 )

   parsed = CHECKER.parse_heading( 'Friday, January 2', today )

   assert parsed == date( today.year + 1, 1, 2 )


def Test_ParseHeading_TestDecemberBeforeJanuary_ExpectPreviousYear() -> None:
   today = date( 2027, 1, 2 )

   parsed = CHECKER.parse_heading( 'Wednesday, December 30', today )

   assert parsed == date( today.year - 1, 12, 30 )


def Test_CheckSchedules_TestClosedToday_ExpectTodayIgnored(
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

   assert result == 0
   assert 'West Caucasian tur' not in output
   assert 'Domestic Goat' not in output
   assert f'Website dates compared from { tomorrow.isoformat() }' in output


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
   assert 'Different days or times: 0' in output
   assert 'Windows which do not align: 0' in output


def Test_CheckSchedules_TestAppTalkAfterWindow_ExpectNoViolation(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( 'Amur Tiger', LOCATION ) ],
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

   assert result == 0
   assert THURSDAY.isoformat() not in output


def Test_CheckSchedules_TestAppOnlyInsideWindow_ExpectAppViolation(
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

   result, output = _check( database, capsys )

   assert result == 1
   assert f'  { TALK }, { LOCATION }' in output
   assert 'Scheduled in the app and not on the website: 1' in output
   assert 'Scheduled on the website and not in the app: 0' in output
   html = _email( output, result )
   assert 'Guardians Talks' in html
   assert f'{ TALK }, { LOCATION }' in html
   assert 'Scheduled in the app and not on the website' in html
   assert 'Website dates compared' not in html


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

   assert result == 1
   assert '  West Caucasian tur, Eurasia' in output
   assert f'  { TALK }, { LOCATION }' not in output
   assert 'Scheduled on the website and not in the app: 1' in output
   html = _email( output, result )
   assert 'West Caucasian tur, Eurasia' in html
   assert 'Scheduled on the website and not in the app' in html
   assert f'{ TALK }, { LOCATION }' not in html
   assert 'Website dates compared' not in html


def Test_CheckSchedules_TestDifferentTime_ExpectDayOrTimeViolation(
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

   assert result == 1
   assert 'Different days or times: 1' in output
   assert 'Windows which do not align: 0' in output
   assert CHECKER.normalize_clock( WEBSITE_CLOCK ) in output
   assert OTHER_CLOCK in output
   html = _email( output, result )
   assert 'Different days or times' in html
   assert 'Website' in html
   assert '1:00 PM Thu' in html
   assert 'App' in html
   assert '11:00 AM Thu' in html
   assert 'Website dates compared' not in html


def Test_CheckSchedules_TestWebsiteWindowLonger_ExpectWindowViolation(
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

   assert result == 1
   assert 'Windows which do not align: 1' in output
   assert 'Different days or times: 0' in output
   assert f'Website dates not in the app: { NEXT_THURSDAY.isoformat() }' in output
   assert 'App dates not on the website' not in output
   html = _email( output, result )
   assert 'Website dates not in the app' in html
   assert NEXT_THURSDAY.isoformat() in html
   assert 'App dates not on the website' not in html
   assert 'Website dates compared' not in html


def Test_CheckSchedules_TestAppWindowLonger_ExpectWindowViolation(
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

   assert result == 1
   assert f'App dates not on the website: { NEXT_THURSDAY.isoformat() }' in output
   assert AFTER_WINDOW.isoformat() not in output
   assert 'Website dates not in the app' not in output
   html = _email( output, result )
   assert 'App dates not on the website' in html
   assert NEXT_THURSDAY.isoformat() in html
   assert 'Website dates not in the app' not in html
   assert 'Website dates compared' not in html


def Test_CheckSchedules_TestMatchingWindow_ExpectNoViolations(
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
   assert AFTER_WINDOW.isoformat() not in output
   assert 'Scheduled in the app and not on the website: 0' in output
   assert 'Windows which do not align: 0' in output
   html = _email( output, result )
   assert 'All clear' in html
   assert 'The website and the app match.' in html
   assert 'Guardians Talks' in html
   assert f'{ TALK }, { LOCATION }' not in html
   assert 'Website dates compared' not in html
