from __future__ import annotations

from datetime import date
from datetime import timedelta
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
import sqlite3
import types

import pytest


AFRICA = 'Africa Restaurant'
SAVANNA = 'Savanna Snack Bar'
TACOS = 'Tundra Tacos'
EURASIA = 'Eurasia Pizza Pizza'
PIZZA = 'Pizza Window'
SHARED_LINK = 'https://www.torontozoo.com/!/pdfs/food/Eurasia%20pizza%20pizza%20menu%202025.pdf'
TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
STEADY = date( 2026, 7, 15 )
SCHEMA = """
CREATE TABLE Restaurant (
   NAME      TEXT NOT NULL,
   MENU_LINK TEXT,
   PRIMARY KEY ( NAME )
);

CREATE TABLE RestaurantStatus (
   RESTAURANT         TEXT NOT NULL,
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
      / 'seasonalRestaurantClosureCheck.py'
   )
   spec = spec_from_file_location( 'seasonal_restaurant_closure_check', path )

   if spec == None or spec.loader == None:
      raise RuntimeError( 'Could not load the restaurant closure check.' )

   module = module_from_spec( spec )
   spec.loader.exec_module( module )
   return module


CHECKER = _load_checker()


def _write_database(
      path: Path,
      restaurants: list[ tuple[ str, str | None ] ],
      closed_for_season: list[ tuple[ str, str | None, str | None ] ],
      curves: list[ tuple[ date, float, float ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Restaurant ( NAME, MENU_LINK ) VALUES ( ?, ? )',
      restaurants,
   )

   for name, start, end in closed_for_season:
      connection.execute(
         """   INSERT INTO RestaurantStatus (
                  RESTAURANT,
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
         ( AFRICA, 'Africa', yesterday.month, yesterday.day, yesterday_value ),
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
         ( AFRICA, 'Africa', scheduled_date.month, scheduled_date.day, today_value ),
      )

   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str, str ] ] ) -> str:
   parts = []

   for href, title, status in cards:
      if href == '':
         parts.append(
            f'<div class="col3">'
            f'<div class="col3title">{ title }</div>'
            f'<span class="opentxt">{ status }</span>'
            f'</div>'
         )
         continue

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
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/savanna.pdf', 'Savanna snack bar', 'Closed For The Season' ),
         ( '/!/pdfs/food/africa.pdf', AFRICA, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { SAVANNA }' in output
   assert AFRICA not in output
   assert 'Closed for the season on the website and not in the app: 1' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestCardWithoutLink_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TACOS, None ) ],
      [ ( TACOS, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', TACOS, 'Closed for the Season' ),
         ( '/!/pdfs/food/ice.pdf', 'Ice Cream Carts', 'Closed for the Season' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert TACOS not in output
   assert 'Ice Cream Carts' not in output
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestUnknownWebsiteCard_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( AFRICA, None ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/ice.pdf', 'Ice Cream Carts', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Ice Cream Carts' not in output
   assert 'Closed for the season on the website and not in the app: 0' in output


def Test_CheckSchedules_TestSharedLink_ExpectBothRestaurantsCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( EURASIA, SHARED_LINK ),
         ( PIZZA, SHARED_LINK ),
      ],
      [
         ( EURASIA, TODAY.isoformat(), None ),
         ( PIZZA, TODAY.isoformat(), None ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/!/pdfs/food/Eurasia pizza pizza menu 2025.pdf',
            'Eurasia Pizza',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert EURASIA not in output
   assert PIZZA not in output


def Test_CheckSchedules_TestSharedLinkOneRestaurant_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( EURASIA, SHARED_LINK ),
         ( PIZZA, SHARED_LINK ),
      ],
      [ ( EURASIA, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/!/pdfs/food/Eurasia pizza pizza menu 2025.pdf',
            'Eurasia Pizza',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { PIZZA }' in output
   assert EURASIA not in output
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
         ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ),
         ( TACOS, None ),
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
      ],
      [
         ( TACOS, TODAY.isoformat(), None ),
         ( AFRICA, None, ended.isoformat() ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/savanna.pdf', SAVANNA, 'Closed For The Season' ),
         ( '/!/pdfs/food/africa.pdf', AFRICA, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert f'  { SAVANNA }' in output
   assert f'  { TACOS }' in output
   assert AFRICA not in output
   assert 'Closed for the season in the app and not on the website: 1' in output


def Test_CheckSchedules_TestOpenThroughPastDate_ExpectWebsiteSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TACOS, None ) ],
      [ ( TACOS, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/tacos.pdf', TACOS, 'Open Weekends Through October 31st' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert TACOS not in output
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
      [ ( TACOS, None ) ],
      [ ( TACOS, through_today.isoformat(), None ) ],
      [ ( through_today, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/tacos.pdf', TACOS, 'Open Weekends Through October 31' ),
      ] ),
   )

   result, output = _check( database, through_today, capsys )

   assert result == 1
   assert f'  { TACOS }' in output
   assert 'Closed for the season in the app and not on the website: 1' in output
   assert 'Closed for the season on the website and not in the app: 0' in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ) ],
      [ ( SAVANNA, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/savanna.pdf', 'Savanna snack bar', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Closed for the season on the website and not in the app: 0' in output
   assert 'Closed for the season in the app and not on the website: 0' in output


def Test_CheckSchedules_TestRampUpAppOnly_ExpectAppExtra(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SAVANNA, None ),
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
      ],
      [ ( SAVANNA, RAMP_UP.isoformat(), None ) ],
      [ ( RAMP_UP, 0.5, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/africa.pdf', AFRICA, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 1
   assert f'  { SAVANNA }' in output
   assert AFRICA not in output
   assert 'ramping up' in output
   assert 'Closed for the season in the app and not on the website: 1' in output
   assert 'on the website and not in the app' not in output


def Test_CheckSchedules_TestSteadyCurves_ExpectNoComparison(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, None ) ],
      [ ( SAVANNA, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/savanna.pdf', SAVANNA, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert SAVANNA not in output
   assert 'not ramping down' in output


def Test_CheckSchedules_TestMissingList_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, None ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, '<html></html>' )

   with pytest.raises( RuntimeError, match='no restaurant list' ):
      CHECKER.check_schedules( database, TODAY )


def Test_CheckSchedules_TestMissingCurves_ExpectError( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [], [], [] )

   with pytest.raises( RuntimeError, match='no seasonal viewability curves' ):
      CHECKER.check_schedules( database, TODAY )
