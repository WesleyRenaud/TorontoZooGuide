from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.seasonal_drinking_fountain_closure_checker import SeasonalDrinkingFountainClosureChecker as CHECKER
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
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

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);
"""




def _write_database(
      path: Path,
      status: tuple[ int, str | None, str | None ] | None,
      curves: list[ tuple[ date, float, float ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )

   if status != None:
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

   for scheduled_date, yesterday_value, today_value in curves:
      yesterday = scheduled_date - timedelta( days=1 )
      connection.execute(
         """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
                  SPECIES,
                  EXHIBIT,
                  MONTH,
                  DAY,
                  VALUE
               ) VALUES ( ?, ?, ?, ?, ? )
         """,
         ( 'Lion', 'Africa', yesterday.month, yesterday.day, yesterday_value ),
      )
      connection.execute(
         """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
                  SPECIES,
                  EXHIBIT,
                  MONTH,
                  DAY,
                  VALUE
               ) VALUES ( ?, ?, ?, ?, ? )
         """,
         ( 'Lion', 'Africa', scheduled_date.month, scheduled_date.day, today_value ),
      )

   connection.commit()
   connection.close()


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


def Test_CheckSchedules_TestWebsiteMessage_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None, [ ( TODAY, 1.0, 0.5 ) ] )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'Closed for the season on the website and not in the app: 1' in output
   assert 'Drinking fountains' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestLegacyNotice_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None, [ ( TODAY, 1.0, 0.5 ) ] )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ], boxes=False ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'Closed for the season on the website and not in the app: 1' in output


def Test_CheckSchedules_TestMaintenanceMessage_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None, [ ( TODAY, 1.0, 0.5 ) ] )
   _install_page(
      monkeypatch,
      _page( [ 'The indoor drinking fountain is closed for maintenance.' ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestAppClosed_ExpectAppExtra(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      ( 1, TODAY.isoformat(), None ),
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 1' in output
   assert 'Drinking fountains' in output


def Test_CheckSchedules_TestBothClosed_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      ( 1, None, None ),
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestEndedStatus_ExpectNotClosed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      ( 1, None, '2026-05-01' ),
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestRampUpAppOnly_ExpectAppExtra(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      ( 1, RAMP_UP.isoformat(), None ),
      [ ( RAMP_UP, 0.5, 1.0 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Ticket warning.' ] ) )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 1
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 1' in output
   assert '  Drinking fountains' in output


def Test_CheckSchedules_TestWebsiteClosedWithoutAppStatus_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, None, [ ( RAMP_UP, 0.5, 1.0 ) ] )
   _install_page( monkeypatch, _page( [ PAST_SEASON_MESSAGE ] ) )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 1
   assert 'Closed for the season on the website and not in the app: 1' in output
   assert '  Drinking fountains' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


