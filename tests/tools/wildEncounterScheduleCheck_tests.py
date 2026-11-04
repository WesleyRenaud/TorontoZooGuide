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


def _load_checker() -> types.ModuleType:
   path = Path( __file__ ).resolve().parents[ 2 ] / 'tools' / 'wildEncounterScheduleCheck.py'
   spec = spec_from_file_location( 'wild_encounter_schedule_check', path )

   if spec == None or spec.loader == None:
      raise RuntimeError( 'Could not load the schedule check.' )

   module = module_from_spec( spec )
   spec.loader.exec_module( module )
   return module


CHECKER = _load_checker()


def _write_database(
      path: Path,
      catalog: list[ tuple[ str, str ] ],
      schedules: list[ tuple[ str, str, str, str ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
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
   first = TODAY + timedelta( days=1 )
   last = SCHEDULE_END - timedelta( days=1 )
   return [ first, first + timedelta( days=1 ), last ]


def _install_web(
      monkeypatch: pytest.MonkeyPatch,
      pages: dict[ str, str ],
      calendars: dict[ str, dict[ str, object ] ] ) -> None:
   def fetch_text( url: str ) -> str:
      return pages[ url ]

   def post_json( url: str, payload: dict[ str, object ] ) -> dict[ str, object ]:
      if url != CHECKER.BOOKING_GRAPHQL_URL:
         raise RuntimeError( url )

      variables = payload[ 'variables' ]

      if not isinstance( variables, dict ):
         raise RuntimeError( 'Missing booking variables.' )

      return calendars[ str( variables[ 'bookingType' ] ) ]

   monkeypatch.setattr( CHECKER, 'fetch_text', fetch_text )
   monkeypatch.setattr( CHECKER, 'post_json', post_json )


def _email( output: str, issues: int ) -> str:
   label = '1 error' if issues == 1 else f'{ issues } errors'
   body = (
      f'{ output }\n'
      f'{ issues } for encounters, 0 for talks, 0 for animals, '
      '0 for attractions, 0 for restaurants, 0 for gift shops, '
      '0 for drinking fountains, 0 for the animal list, '
      '0 for the attraction list, 0 for the restaurant list, '
      '0 for the gift shop list, 0 for zoo hours\n\n'
      f'{ label }\n'
   )
   return email_summary.render_html( body, 1 if issues else 0 )


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


def _giraffe_pages( website_time: str ) -> dict[ str, str ]:
   return {
      CHECKER.WEBSITE_SCHEDULE_URL: _schedule_page( [ ( website_time, GIRAFFE ) ] ),
      GIRAFFE_LINK: _booking_page( GIRAFFE_TOUR ),
   }


def Test_CheckSchedules_TestAppOnlyEncounter_ExpectAppViolation(
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
   assert result == 1
   assert 'Scheduled in the app and not on the website: 1' in output
   assert f'  { KANGAROO }' in output
   assert GIRAFFE not in output
   assert 'Scheduled on the website and not in the app: 0' in output
   assert 'Different days or times: 0' in output
   assert 'Windows which do not align: 0' in output
   html = _email( output, result )
   assert 'Kangaroo' in html
   assert 'Scheduled in the app and not on the website' in html
   assert 'Booking dates compared' not in html
   assert GIRAFFE not in html


def Test_CheckSchedules_TestWebsiteOnlyEncounter_ExpectWebsiteViolation(
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
   pages[ CHECKER.WEBSITE_SCHEDULE_URL ] = _schedule_page( [
      ( WEBSITE_CLOCK, GIRAFFE ),
      ( WEBSITE_CLOCK, SNOW_LEOPARD_WEBSITE ),
   ] )
   _install_web(
      monkeypatch,
      pages,
      { GIRAFFE_TOUR: _enabled_dates( _matched_dates() ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 1
   assert 'Scheduled on the website and not in the app: 1' in output
   assert f'  { SNOW_LEOPARD }' in output
   assert f'  { SNOW_LEOPARD_WEBSITE }' not in output
   assert 'Scheduled in the app and not on the website: 0' in output
   assert 'Windows which do not align: 0' in output
   html = _email( output, result )
   assert SNOW_LEOPARD in html
   assert 'Scheduled on the website and not in the app' in html
   assert 'Booking dates compared' not in html


def Test_CheckSchedules_TestDifferentTime_ExpectDayOrTimeViolation(
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
   assert result == 1
   assert 'Different days or times: 1' in output
   assert f'  { GIRAFFE }' in output
   assert CHECKER.normalize_clock( OTHER_CLOCK ) in output
   assert CHECKER.normalize_clock( CLOCK ) in output
   assert 'Windows which do not align: 0' in output
   html = _email( output, result )
   assert 'Different days or times' in html
   assert 'Website' in html
   assert '2:00 PM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in html
   assert 'App' in html
   assert '11:00 AM Sun, Mon, Tue, Wed, Thu, Fri, Sat' in html
   assert 'Booking dates compared' not in html


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
   assert result == 1
   assert 'Windows which do not align: 1' in output
   assert f'  { GIRAFFE }' in output
   assert 'Bookable dates not in the app: ' in output
   assert CHECKER.format_date_span( extra_start, extra_end ) in output
   assert 'App dates not bookable' not in output
   assert 'Different days or times: 0' in output
   html = _email( output, result )
   assert 'Bookable dates not in the app' in html
   assert '2026-11-05 through 2026-11-06' in html
   assert 'Booking dates compared' not in html


def Test_CheckSchedules_TestAppWindowLonger_ExpectWindowViolation(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   matched = _matched_dates()
   missing_start = matched[ 0 ] + timedelta( days=1 )
   missing_end = matched[ -1 ]
   _giraffe_database( database, CLOCK )
   _install_web(
      monkeypatch,
      _giraffe_pages( WEBSITE_CLOCK ),
      { GIRAFFE_TOUR: _enabled_dates( [ matched[ 0 ] ] ) } )

   result = CHECKER.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 1
   assert 'Windows which do not align: 1' in output
   assert f'  { GIRAFFE }' in output
   assert 'App dates not bookable: ' in output
   assert CHECKER.format_date_span( missing_start, missing_end ) in output
   assert 'Bookable dates not in the app' not in output
   assert 'Different days or times: 0' in output
   html = _email( output, result )
   assert 'App dates not bookable' in html
   assert '2026-11-03 through 2026-11-04' in html
   assert 'Bookable dates not in the app' not in html
   assert 'Booking dates compared' not in html


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
   assert 'Scheduled in the app and not on the website: 0' in output
   assert 'Scheduled on the website and not in the app: 0' in output
   assert 'Different days or times: 0' in output
   assert 'Windows which do not align: 0' in output
   html = _email( output, result )
   assert 'All clear' in html
   assert 'The website and the app match.' in html
   assert GIRAFFE not in html
   assert 'Booking dates compared' not in html
