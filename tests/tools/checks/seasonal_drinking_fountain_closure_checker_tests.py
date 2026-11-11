from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from tools.checks.check_report import CheckReport
from tools.checks.seasonal_drinking_fountain_closure_checker import SeasonalDrinkingFountainClosureChecker as CHECKER
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
JUNE = date( 2026, 6, 1 )
PAST_SEASON_MESSAGE = (
   'Outdoor water fountains and filling stations are closed for the season '
   'due to cold temperatures.'
)
SCHEMA = """
CREATE TABLE DrinkingFountainStatus (
   IS_CLOSED       BOOL NOT NULL,
   START_DATE      DATE,
   END_DATE        DATE,
   CLOSED_MESSAGE  TEXT
);
"""



def _write_database(
      path: Path,
      status: tuple[ int, str | None, str | None ] | None ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )

   if status is not None:
      is_closed, start, end = status
      connection.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               ) VALUES ( ?, ?, ?, ? )
         """,
         ( is_closed, start, end, 'The drinking fountains are closed for the season.' ),
      )

   connection.commit()
   connection.close()


def _stored( path: Path ) -> tuple[ int, str | None, str | None ] | None:
   connection = sqlite3.connect( path )
   row = connection.execute(
      """   SELECT IS_CLOSED, START_DATE, END_DATE
            FROM DrinkingFountainStatus
      """
   ).fetchone()
   connection.close()
   return None if row is None else ( row[ 0 ], row[ 1 ], row[ 2 ] )


def _page( notices: list[ str ], *, boxes: bool = True ) -> str:
   if boxes:
      bodies = ''.join(
         f'<div class="box scrolling-title" id="{ index }"><p>{ notice }</p></div>'
         for index, notice in enumerate( notices, start=1 )
      )
   else:
      bodies = ''.join( f'<span><p>{ notice }</p></span><hr />' for notice in notices )

   return (
      '<h2 id="notices">Notices &amp; Closures</h2>'
      f'{ bodies }'
      '<h2 id="animals2">Animals Not Currently Viewable</h2>'
   )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = CHECKER.check_schedules( database, today )
   return result, capsys.readouterr().out


def _span( start: date, end: date, closed: bool ) -> str:
   key = 'checks.setClosedForSeasonFrom' if closed else 'checks.setOpenForSeasonFrom'
   return (
      CheckReport.text( key )
      + DateValues.format_display_date_value( start )
      + CheckReport.text( 'checks.dateThrough' )
      + DateValues.format_display_date_value( end )
      + CheckReport.text( 'checks.period' )
   )



def Test_CheckSchedules_TestWebsiteClosedInNovember_ExpectClosedUntilApril(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 1 ) in output
   assert _span( TODAY, date( 2027, 4, 30 ), True ) in output
   assert _stored( database ) == ( 1, TODAY.isoformat(), '2027-04-30' )


def Test_CheckSchedules_TestLegacyNotice_ExpectClosedUntilApril(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ], boxes=False ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert _span( TODAY, date( 2027, 4, 30 ), True ) in output


def Test_CheckSchedules_TestClosedWindowAlreadySet_ExpectNoChange(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, ( 1, '2026-11-01', '2027-04-30' ) )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   assert _stored( database ) == ( 1, '2026-11-01', '2027-04-30' )


def Test_CheckSchedules_TestClosedWithoutEnd_ExpectEndKeptStart(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, ( 1, '2026-11-01', None ) )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert _span( date( 2026, 11, 1 ), date( 2027, 4, 30 ), True ) in output
   assert _stored( database ) == ( 1, '2026-11-01', '2027-04-30' )


def Test_CheckSchedules_TestClosedInMarch_ExpectApril30(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 0
   assert _span( RAMP_UP, date( 2026, 4, 30 ), True ) in output
   assert _stored( database ) == ( 1, RAMP_UP.isoformat(), '2026-04-30' )


def Test_CheckSchedules_TestClosedInJune_ExpectTwoWeeks(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, JUNE, capsys )

   assert result == 0
   assert _span( JUNE, CalendarDates.two_weeks_later( JUNE ), True ) in output
   assert _stored( database ) == ( 1, JUNE.isoformat(), '2026-06-15' )


def Test_CheckSchedules_TestOpenInJune_ExpectOctober31(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, JUNE, capsys )

   assert result == 0
   assert _span( JUNE, date( 2026, 10, 31 ), False ) in output
   assert _stored( database ) == ( 0, JUNE.isoformat(), '2026-10-31' )


def Test_CheckSchedules_TestOpenInNovember_ExpectTwoWeeks(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, ( 1, TODAY.isoformat(), None ) )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert _span( TODAY, CalendarDates.two_weeks_later( TODAY ), False ) in output
   assert _stored( database ) == ( 0, TODAY.isoformat(), '2026-11-16' )


def Test_CheckSchedules_TestMaintenanceMessage_ExpectOpenWindow(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None )
   _install_page(
      monkeypatch,
      _page( [ 'The indoor drinking fountain is closed for maintenance.' ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert _span( TODAY, CalendarDates.two_weeks_later( TODAY ), False ) in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) not in output


def Test_CheckSchedules_TestOpenWindowAlreadySet_ExpectNoChange(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, ( 0, JUNE.isoformat(), '2026-10-31' ) )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, JUNE, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   assert _stored( database ) == ( 0, JUNE.isoformat(), '2026-10-31' )
