from __future__ import annotations

from datetime import date
from datetime import timedelta
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
import sqlite3
import types

import pytest


SPLASH = 'Splash Island'
CLIMB = 'Gorilla Climb Ropes Course'
FRONT_GATES = 'Face Painting, Caricatures and Henna! - Front Gates'
TUNDRA = 'Face Painting, Caricatures and Henna! - Tundra Trek'
KANGAROO = 'Kangaroo Walk-Thru'
KIDS_ZOO = 'Kids Zoo'
FACE_PAINTING_LINK = 'https://www.torontozoo.com/tz/facepainting'
TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
STEADY = date( 2026, 7, 15 )
SCHEMA = """
CREATE TABLE Attraction (
   NAME      TEXT NOT NULL,
   INFO_LINK TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);

CREATE TABLE AttractionStatus (
   ATTRACTION         TEXT NOT NULL,
   IS_CLOSED          BOOL NOT NULL,
   CLOSED_MESSAGE     TEXT,
   CLOSED_START       DATE,
   CLOSED_END         DATE,
   CLOSED_FOR_SEASON  BOOL NOT NULL
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

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);
"""


def _load_checker() -> types.ModuleType:
   path = (
      Path( __file__ ).resolve().parents[ 2 ]
      / 'tools'
      / 'seasonalAttractionClosureCheck.py'
   )
   spec = spec_from_file_location( 'seasonal_attraction_closure_check', path )

   if spec == None or spec.loader == None:
      raise RuntimeError( 'Could not load the attraction closure check.' )

   module = module_from_spec( spec )
   spec.loader.exec_module( module )
   return module


CHECKER = _load_checker()


def _write_database(
      path: Path,
      attractions: list[ tuple[ str, str ] ],
      closed_for_season: list[ tuple[ str, str | None, str | None ] ],
      curves: list[ tuple[ date, float, float ] ],
      closures: list[ tuple[ str, str | None, str | None, bool ] ] | None = None ) -> None:
   if closures == None:
      closures = []

   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Attraction ( NAME, INFO_LINK ) VALUES ( ?, ? )',
      attractions,
   )

   for name, start, end in closed_for_season:
      connection.execute(
         """   INSERT INTO AttractionStatus (
                  ATTRACTION,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               ) VALUES ( ?, 1, ?, ?, 1 )
         """,
         ( name, start, end ),
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
         ( SPLASH, 'Discovery Zone', yesterday.month, yesterday.day, yesterday_value ),
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
         ( SPLASH, 'Discovery Zone', scheduled_date.month, scheduled_date.day, today_value ),
      )

   for exhibit, start, end, for_season in closures:
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
         ( exhibit, start, end, 1 if for_season else 0 ),
      )

   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str, str ] ] ) -> str:
   parts = []

   for href, title, status in cards:
      parts.append(
         f'<a class="col3" href="{ href }">'
         f'<div class="col3title">{ title }</div>'
         f'<span class="opentxt">{ status }</span>'
         '</a>'
      )

   return ''.join( parts )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( CHECKER, 'fetch_text', fetch_text )


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
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', 'Splash island', 'Closed For The Season' ),
         ( '/tz/kangaroo', KANGAROO, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { SPLASH }' in output
   assert KANGAROO not in output
   assert 'Closed for the season on the website and not in the app: 1' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestExhibitClosedForSeason_ExpectExhibitCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
      [ ( KIDS_ZOO, TODAY.isoformat(), None, True ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/kidszoo', 'Kids&nbsp;Zoo', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert KIDS_ZOO not in output
   assert 'Closed for the season on the website and not in the app: 0' in output


def Test_CheckSchedules_TestExhibitClosedNotForSeason_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
      [ ( KIDS_ZOO, TODAY.isoformat(), None, False ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/kidszoo', KIDS_ZOO, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { KIDS_ZOO }' in output
   assert 'Closed for the season on the website and not in the app: 1' in output


def Test_CheckSchedules_TestSharedLink_ExpectBothLocationsCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( FRONT_GATES, FACE_PAINTING_LINK ),
         ( TUNDRA, FACE_PAINTING_LINK ),
      ],
      [
         ( FRONT_GATES, TODAY.isoformat(), None ),
         ( TUNDRA, TODAY.isoformat(), None ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/tz/facepainting',
            'Face Painting, Body Art, and Henna!',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert FRONT_GATES not in output
   assert TUNDRA not in output


def Test_CheckSchedules_TestSharedLinkOneLocation_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( FRONT_GATES, FACE_PAINTING_LINK ),
         ( TUNDRA, FACE_PAINTING_LINK ),
      ],
      [ ( FRONT_GATES, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/tz/facepainting',
            'Face Painting, Body Art, and Henna!',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { TUNDRA }' in output
   assert FRONT_GATES not in output
   assert 'Closed for the season on the website and not in the app: 1' in output


def Test_CheckSchedules_TestRampDownAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   ended = TODAY - timedelta( days=1 )
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ),
         ( CLIMB, 'https://www.torontozoo.com/tz/gorillaclimb' ),
      ],
      [
         ( KANGAROO, TODAY.isoformat(), None ),
         ( CLIMB, None, ended.isoformat() ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH, 'Closed For The Season' ),
         ( '/tz/kangaroo', KANGAROO, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert f'  { SPLASH }' in output
   assert f'  { KANGAROO }' in output
   assert CLIMB not in output
   assert 'Closed for the season in the app and not on the website: 1' in output


def Test_CheckSchedules_TestOpenThroughPastDate_ExpectWebsiteSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ) ],
      [ ( KANGAROO, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/kangaroo', KANGAROO, 'Open Weekends Through October 31st' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert KANGAROO not in output
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestOpenThroughToday_ExpectStillOpen(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   through_today = date( 2026, 10, 31 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ) ],
      [ ( KANGAROO, through_today.isoformat(), None ) ],
      [ ( through_today, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/kangaroo', KANGAROO, 'Open Weekends Through October 31' ),
      ] ),
   )

   result, output = _check( database, through_today, capsys )

   assert result == 1
   assert f'  { KANGAROO }' in output
   assert 'Closed for the season in the app and not on the website: 1' in output
   assert 'Closed for the season on the website and not in the app: 0' in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [ ( SPLASH, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/splash', 'Splash island', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestRampUp_ExpectNoComparison(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [ ( SPLASH, RAMP_UP.isoformat(), None ) ],
      [ ( RAMP_UP, 0.5, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/splash', CLIMB, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 0
   assert SPLASH not in output
   assert CLIMB not in output
   assert 'not ramping down' in output


def Test_CheckSchedules_TestSteadyCurves_ExpectNoComparison(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [ ( SPLASH, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/splash', SPLASH, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert SPLASH not in output
   assert 'not ramping down' in output


def Test_CheckSchedules_TestMissingList_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, '<html></html>' )

   with pytest.raises( RuntimeError, match='no attraction list' ):
      CHECKER.check_schedules( database, TODAY )


def Test_CheckSchedules_TestMissingCurves_ExpectError( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [], [], [] )

   with pytest.raises( RuntimeError, match='no seasonal viewability curves' ):
      CHECKER.check_schedules( database, TODAY )
