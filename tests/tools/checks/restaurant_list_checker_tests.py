from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.restaurant_list_checker import RestaurantListChecker as restaurant_list_checker
from tools.checks.website_page import WebsitePage


AFRICA = 'Africa Restaurant'
SAVANNA = 'Savanna Snack Bar'
TACOS = 'Tundra Tacos'
THORNTREE = 'Thorntree Café'
PALGONG = 'Caribou Café Palgong'
SHARED_LINK = 'https://www.torontozoo.com/!/pdfs/food/Palgong-Menu.pdf'
TODAY = date( 2026, 11, 3 )
SCHEMA = """
CREATE TABLE Restaurant (
   NAME TEXT NOT NULL,
   LOCATION TEXT,
   SUB_LOCATION TEXT,
   DESCRIPTION TEXT NOT NULL DEFAULT '',
   MENU_LINK TEXT,
   X_COORD FLOAT NOT NULL DEFAULT 0,
   Y_COORD FLOAT NOT NULL DEFAULT 0,
   PRIMARY KEY ( NAME )
);
CREATE TABLE RestaurantDaySeasonalAvailabilityMultiplier (
   RESTAURANT TEXT NOT NULL,
   MONTH INTEGER NOT NULL,
   DAY INTEGER NOT NULL,
   WEEKDAY_VALUE FLOAT NOT NULL,
   WEEKEND_HOLIDAY_VALUE FLOAT NOT NULL
);
CREATE TABLE RestaurantOpeningSchedule (
   RESTAURANT TEXT,
   SCHEDULE_START_DATE TEXT,
   SCHEDULE_END_DATE TEXT,
   MONDAY INTEGER,
   TUESDAY INTEGER,
   WEDNESDAY INTEGER,
   THURSDAY INTEGER,
   FRIDAY INTEGER,
   SATURDAY INTEGER,
   SUNDAY INTEGER,
   HOLIDAYS_ONLY INTEGER,
   SCHEDULE_MESSAGE TEXT
);
CREATE TABLE RestaurantScheduleOverride (
   RESTAURANT TEXT,
   OVERRIDE_START_DATE TEXT,
   OVERRIDE_END_DATE TEXT,
   IS_CLOSED INTEGER,
   OVERRIDE_MESSAGE TEXT
);
CREATE TABLE RestaurantStatus (
   RESTAURANT TEXT,
   IS_CLOSED INTEGER,
   CLOSED_START TEXT,
   CLOSED_END TEXT,
   CLOSED_MESSAGE TEXT,
   CLOSED_FOR_SEASON INTEGER
);
"""


def _write_database(
      path: Path,
      restaurants: list[ tuple[ str, str | None ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Restaurant ( NAME, MENU_LINK ) VALUES ( ?, ? )',
      restaurants,
   )
   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str ] ] ) -> str:
   parts = [ '<a href="/!/pdfs/food/other.pdf">Pizza Window</a>' ]

   for href, title in cards:
      if href == '':
         parts.append(
            f'<div class="col3">'
            f'<div class="col3title">{ title }</div>'
            '<span class="opentxt">Open Daily</span>'
            '</div>'
         )
         continue

      parts.append(
         f'<a class="col3" href="{ href }">'
         f'<div class="col3title">{ title }</div>'
         '<span class="opentxt">Open Daily</span>'
         '</a>'
      )

   return ''.join( parts )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = restaurant_list_checker.check_lists( database, today )
   return result, capsys.readouterr().out


def Test_CheckLists_TestWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ) ] )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/africa.pdf', AFRICA ),
         ( '/!/pdfs/food/ice.pdf', 'Discovery Grill' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output
   assert '  Discovery Grill' in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output
   assert 'Pizza Window' not in output


def Test_CheckLists_TestAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
         ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ),
      ],
   )
   _install_page( monkeypatch, _page( [ ( '/!/pdfs/food/africa.pdf', AFRICA ) ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
   assert f'  { SAVANNA }' in output
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output


def Test_CheckLists_TestNormalizedNames_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
         ( "Singh's Trini Vibes", None ),
         ( 'Tundra Tacos (Seasonal)', None ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/other-africa.pdf', 'Africa-Restaurant' ),
         ( '', 'Singh’s Trini Vibes' ),
         ( '', 'Tundra Tacos' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


def Test_CheckLists_TestCardWithoutHours_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( "Wolf's Den Café", 'https://www.torontozoo.com/!/pdfs/food/wolf.pdf' ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/Wolf%20Den%20Menu.pdf', "Wolf's Den Café" ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert "Wolf's Den Café" not in output


def Test_CheckLists_TestDifferentTitle_ExpectBothSides(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/Savanna%20Menu.pdf?' ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/Savanna Menu.pdf?', 'Snack Hut' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert '  Snack Hut' in output
   assert f'  { SAVANNA }' in output


def Test_CheckLists_TestDifferentTitles_ExpectEachMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
         ( THORNTREE, SHARED_LINK ),
         ( PALGONG, SHARED_LINK ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/africa.pdf', AFRICA ),
         ( '/!/pdfs/food/Palgong-Menu.pdf', 'Palgong Tea' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 3
   assert '  Palgong Tea' in output
   assert f'  { THORNTREE }' in output
   assert f'  { PALGONG }' in output
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 2 ) in output


def Test_CheckLists_TestSharedMenuNamedCard_ExpectOtherAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( THORNTREE, SHARED_LINK ),
         ( PALGONG, SHARED_LINK ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/Palgong-Menu.pdf', THORNTREE ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { PALGONG }' in output
   assert THORNTREE not in output
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output


def Test_CheckLists_TestEmptyHrefDoesNotMatchNullLink_ExpectBothSides(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( TACOS, None ) ] )
   _install_page( monkeypatch, _page( [ ( '', 'Discovery Grill' ) ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert '  Discovery Grill' in output
   assert f'  { TACOS }' in output


def Test_CheckLists_TestBothSides_ExpectIssueCount(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
         ( SAVANNA, None ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/africa.pdf', AFRICA ),
         ( '', 'Discovery Grill' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert output.startswith( f'Restaurant list check for { TODAY.isoformat() }.' )
   assert '  Discovery Grill' in output
   assert f'  { SAVANNA }' in output


@pytest.mark.parametrize(
   'name',
   sorted( restaurant_list_checker.ALLOWED_WEBSITE_ONLY_RESTAURANTS ),
)
def Test_CheckLists_TestAllowedWebsiteRestaurant_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch,
      name: str ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ) ] )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/africa.pdf', AFRICA ),
         ( '/!/pdfs/food/ice.pdf', name ),
         ( '', 'Discovery Grill' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { name }' not in output
   assert '  Discovery Grill' in output
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output


def Test_CheckLists_TestAllowedRestaurantMissingFromWebsite_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ),
         ( 'Ice Cream Carts', 'https://www.torontozoo.com/!/pdfs/food/ice.pdf' ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/africa.pdf', AFRICA ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert '  Ice Cream Carts' in output
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
