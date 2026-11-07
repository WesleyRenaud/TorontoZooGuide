from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.seasonal_animal_off_display_checker import SeasonalAnimalOffDisplayChecker as CHECKER
from tools.checks.website_page import WebsitePage


STORK = 'Marabou Stork'
TORTOISE = 'African Spurred Tortoise'
HAWK = "Harris's Hawk"
TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
STEADY = date( 2026, 7, 15 )
SCHEMA = """
CREATE TABLE Animal (
   SPECIES TEXT NOT NULL,
   PRIMARY KEY ( SPECIES )
);

CREATE TABLE AnimalStatus (
   SPECIES                 TEXT NOT NULL,
   EXHIBIT                 TEXT NOT NULL,
   IS_OFF_DISPLAY          BOOL NOT NULL,
   VIEWING_SCOPE           TEXT NOT NULL,
   OFF_DISPLAY_MESSAGE     TEXT,
   OFF_DISPLAY_START       DATE,
   OFF_DISPLAY_END         DATE,
   OFF_DISPLAY_FOR_SEASON  BOOL NOT NULL
);

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);

CREATE TABLE Exhibit (
   NAME TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);

CREATE TABLE ExhibitStatus (
   EXHIBIT            TEXT NOT NULL,
   IS_CLOSED          BOOL NOT NULL,
   CLOSED_MESSAGE     TEXT,
   CLOSED_START       DATE,
   CLOSED_END         DATE,
   CLOSED_FOR_SEASON  BOOL NOT NULL
);
"""




def _write_database(
      path: Path,
      species: list[ str ],
      off_season: list[ tuple[ str, str, str | None ] ],
      curves: list[ tuple[ date, float, float ] ],
      closures: list[ tuple[ str, str | None, str | None, bool ] ] | None = None ) -> None:
   if closures == None:
      closures = []

   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Animal ( SPECIES ) VALUES ( ? )',
      [ ( name, ) for name in species ],
   )

   for name, start, end in off_season:
      connection.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  VIEWING_SCOPE,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_FOR_SEASON
               ) VALUES ( ?, ?, 1, ?, ?, ?, 1 )
         """,
         ( name, 'Africa Savanna', name, start, end ),
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
         ( STORK, 'Africa Savanna', yesterday.month, yesterday.day, yesterday_value ),
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
         ( STORK, 'Africa Savanna', scheduled_date.month, scheduled_date.day, today_value ),
      )

   for exhibit, start, end, closed_for_season in closures:
      connection.execute(
         'INSERT INTO Exhibit ( NAME ) VALUES ( ? )',
         ( exhibit, ),
      )
      connection.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               ) VALUES ( ?, 1, ?, ?, ? )
         """,
         ( exhibit, start, end, 1 if closed_for_season else 0 ),
      )

   connection.commit()
   connection.close()


def _page( animals: list[ str ], section: str = 'Africa Savanna' ) -> str:
   cards = []

   for name in animals:
      href = name.replace( ' ', '%20' )
      cards.append(
         f'<a href="/animals/{ href }">'
         '<span class="line2 status sseason">Off for the Season</span>'
         '</a>'
      )

   cards.append(
      '<a href="/animals/Brush-tailed%20bettong">'
      '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
      '</a>'
   )
   return (
      '<h2>Animals Not Currently Viewable</h2>'
      f'<div class="atitle scrolling-title" id="{ section }">'
      + ''.join( cards )
      + '</div>'
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


def Test_CheckSchedules_TestRampDownWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ STORK, HAWK ], [], [ ( TODAY, 1.0, 0.5 ) ] )
   _install_page(
      monkeypatch,
      _page( [ 'Marabou stork' ] ).replace(
         '</div>',
         '<a href="/animals/Harris&#39;s%20hawk">'
         '<span class="line2 status sseason">Off for the Season</span></a></div>',
         1,
      ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert '  Marabou stork' in output
   assert "  Harris's hawk" in output
   assert '&#39;' not in output
   assert 'Off for the season on the website and not in the app: 2' in output
   assert 'Off for the season in the app and not on the website: 0' in output
   assert 'Brush-tailed bettong' not in output


def Test_CheckSchedules_TestExhibitClosedForSeason_ExpectAnimalsCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ HAWK ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
      [ ( 'Kids Zoo', TODAY.isoformat(), None, True ) ],
   )
   _install_page( monkeypatch, _page( [ "Harris's hawk" ], 'Kids Zoo' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert HAWK not in output
   assert 'Off for the season on the website and not in the app: 0' in output


def Test_CheckSchedules_TestExhibitClosedNotForSeason_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ HAWK ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
      [ ( 'Kids Zoo', TODAY.isoformat(), None, False ) ],
   )
   _install_page( monkeypatch, _page( [ "Harris's hawk" ], 'Kids Zoo' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert "  Harris's hawk" in output
   assert 'Off for the season on the website and not in the app: 1' in output


def Test_CheckSchedules_TestRampDownAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   ended = TODAY - timedelta( days=1 )
   _write_database(
      database,
      [ STORK, TORTOISE ],
      [
         ( STORK, TODAY.isoformat(), None ),
         ( TORTOISE, None, ended.isoformat() ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { STORK }' in output
   assert TORTOISE not in output
   assert 'Off for the season in the app and not on the website: 1' in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK ],
      [ ( STORK, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Marabou stork' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Off for the season on the website and not in the app: 0' in output
   assert 'Off for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestDifferentAnimalsOffDisplay_ExpectBoth(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK, TORTOISE ],
      [ ( STORK, RAMP_UP.isoformat(), None ) ],
      [ ( RAMP_UP, 0.5, 1.0 ) ],
   )
   _install_page( monkeypatch, _page( [ TORTOISE ] ) )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 2
   assert f'  { STORK }' in output
   assert f'  { TORTOISE }' in output
   assert 'Off for the season on the website and not in the app: 1' in output
   assert 'Off for the season in the app and not on the website: 1' in output


def Test_CheckSchedules_TestOffDisplayOnSteadyDate_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK ],
      [ ( STORK, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 1.0 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Marabou stork' ] ) )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert STORK not in output
   assert 'Off for the season on the website and not in the app: 0' in output
   assert 'Off for the season in the app and not on the website: 0' in output
