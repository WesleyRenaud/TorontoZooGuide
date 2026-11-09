from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.seasonal_restaurant_closure_checker import SeasonalRestaurantClosureChecker as CHECKER
from tools.checks.seasonal_restaurant_comparison import SeasonalRestaurantComparison
from tools.checks.website_page import WebsitePage


AFRICA = 'Africa Restaurant'
SAVANNA = 'Savanna Snack Bar'
TACOS = 'Tundra Tacos'
EURASIA = 'Eurasia Pizza Pizza'
PIZZA = 'BeaverTails Trailer'
SHARED_LINK = 'https://www.torontozoo.com/!/pdfs/food/Eurasia%20pizza%20pizza%20menu%202025.pdf'
COCOA = 'Cocoa Flow'
TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
STEADY = date( 2026, 7, 15 )
APRIL = date( 2027, 4, 30 )
UNTIL_MONTHS = {
   SAVANNA: 4,
   TACOS: 3,
   EURASIA: 4,
   PIZZA: 4,
   COCOA: 2,
}
SCHEMA = """
CREATE TABLE Restaurant (
   NAME      TEXT NOT NULL,
   MENU_LINK TEXT,
   CLOSED_FOR_SEASON_UNTIL_MONTH INTEGER,
   PRIMARY KEY ( NAME )
);

CREATE TABLE RestaurantStatus (
   RESTAURANT         TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED          BOOL NOT NULL,
   CLOSED_MESSAGE     TEXT,
   CLOSED_START       DATE,
   CLOSED_END         DATE,
   CLOSED_FOR_SEASON  BOOL NOT NULL
);
"""




def _write_database(
      path: Path,
      restaurants: list[ tuple[ str, str | None ] ],
      closed_for_season: list[ tuple[ str, str | None, str | None ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      """   INSERT INTO Restaurant (
               NAME,
               MENU_LINK,
               CLOSED_FOR_SEASON_UNTIL_MONTH
            ) VALUES ( ?, ?, ? )
      """,
      [
         ( name, link, UNTIL_MONTHS.get( name ) )
         for name, link in restaurants
      ],
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

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, today )
   return result, capsys.readouterr().out


def _season_row( database: Path, name: str ) -> tuple[ int, str | None, str | None, int ] | None:
   connection = sqlite3.connect( database )
   row = connection.execute(
      """   SELECT
               IS_CLOSED,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM RestaurantStatus
            WHERE RESTAURANT = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()

   if row == None:
      return None

   return ( row[ 0 ], row[ 1 ], row[ 2 ], row[ 3 ] )


def Test_CheckSchedules_TestWebsiteOnly_ExpectClosedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ) ],
      [],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/savanna.pdf', 'Savanna snack bar', 'Closed For The Season' ),
         ( '/!/pdfs/food/africa.pdf', AFRICA, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { SAVANNA }' in output
   assert 'images/details/restaurants/savanna-snack-bar.png' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert 'April 30, 2027' in output
   assert _season_row( database, SAVANNA ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert AFRICA not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestCardWithoutLink_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TACOS, None ) ],
      [ ( TACOS, TODAY.isoformat(), None ) ],
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
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestBlankLink_ExpectNameMatchOnly(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   pretzel = 'Americas Pretzel Bar'
   _write_database(
      database,
      [
         ( TACOS, None ),
         ( pretzel, None ),
      ],
      [ ( TACOS, TODAY.isoformat(), None ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', TACOS, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert pretzel not in output
   assert TACOS not in output


def Test_CheckSchedules_TestUnknownWebsiteCard_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( AFRICA, None ) ],
      [],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/ice.pdf', 'Ice Cream Carts', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Ice Cream Carts' not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output


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


def Test_CheckSchedules_TestSharedLinkOneRestaurant_ExpectClosedForSeason(
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
   assert f'  { PIZZA }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert _season_row( database, PIZZA ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert EURASIA not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output


def Test_CheckSchedules_TestWebsiteAndAppMisses_ExpectOpenedAndClosed(
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
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/savanna.pdf', SAVANNA, 'Closed For The Season' ),
         ( '/!/pdfs/food/africa.pdf', AFRICA, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { SAVANNA }' in output
   assert f'  { TACOS }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, SAVANNA ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert _season_row( database, TACOS ) == None
   assert AFRICA not in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestOpenThroughPastDate_ExpectWebsiteSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TACOS, None ) ],
      [ ( TACOS, TODAY.isoformat(), None ) ],
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
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestOpenThroughToday_ExpectOpenedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   through_today = date( 2026, 10, 31 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( TACOS, None ) ],
      [ ( TACOS, through_today.isoformat(), None ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/!/pdfs/food/tacos.pdf', TACOS, 'Open Weekends Through October 31' ),
      ] ),
   )

   result, output = _check( database, through_today, capsys )

   assert result == 0
   assert f'  { TACOS }' in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, TACOS ) == None
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output


def Test_CheckSchedules_TestMatchingClosure_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ) ],
      [ ( SAVANNA, TODAY.isoformat(), None ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/savanna.pdf', 'Savanna snack bar', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestDifferentRestaurantsClosed_ExpectBothCorrected(
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
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/africa.pdf', AFRICA, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 0
   assert f'  { SAVANNA }' in output
   assert f'  { AFRICA }' in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert CheckReport.text( 'checks.extendedClosedForSeasonThrough' ) in output
   assert 'March 22, 2026' in output
   assert _season_row( database, SAVANNA ) == None
   assert _season_row( database, AFRICA ) == ( 1, RAMP_UP.isoformat(), '2026-03-22', 1 )
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonReturningSoon', 1 ) in output


def Test_CheckSchedules_TestClosedOnSteadyDate_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SAVANNA, None ) ],
      [ ( SAVANNA, STEADY.isoformat(), None ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/savanna.pdf', SAVANNA, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert SAVANNA not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_ParseWebsiteRestaurants_TestMissingOpeningStatus_ExpectOmitted() -> None:
   page = (
      '<a class="col3" href="/wolfs">'
      '<div class="col3title">Wolf\'s Den Cafe</div>'
      '<b>Weekends</b>'
      '</a>'
      '<a class="col3" href="/savanna">'
      f'<div class="col3title">{ SAVANNA }</div>'
      '<span class="opentxt">Closed for the Season</span>'
      '</a>'
   )

   listings = SeasonalRestaurantComparison.parse_website_restaurants( page, TODAY )

   assert [ listing.title for listing in listings ] == [ SAVANNA ]


def Test_CheckSchedules_TestCocoaFlowWebsiteOnly_ExpectDetailImage(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( COCOA, None ) ], [] )
   _install_page(
      monkeypatch,
      _page( [ ( '', COCOA, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'images/details/restaurants/cocoa-flow.png' in output
   assert '  Cocoa Flow · Front Courtyard' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert 'February 28, 2027' in output
   assert _season_row( database, COCOA ) == ( 1, TODAY.isoformat(), '2027-02-28', 1 )


def Test_CheckSchedules_TestSeasonEndToday_ExpectExtendedOneWeek(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   start = '2026-11-08'
   _write_database(
      database,
      [ ( SAVANNA, 'https://www.torontozoo.com/!/pdfs/food/savanna.pdf' ) ],
      [ ( SAVANNA, start, APRIL.isoformat() ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/savanna.pdf', SAVANNA, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, APRIL, capsys )

   assert result == 0
   assert CheckReport.text( 'checks.extendedClosedForSeasonThrough' ) in output
   assert 'May 8, 2027' in output
   assert _season_row( database, SAVANNA ) == ( 1, start, '2027-05-08', 1 )
   assert CheckReport.category_line( 'checks.closedForSeasonReturningSoon', 1 ) in output


def Test_CheckSchedules_TestNoUntilMonth_ExpectCrash(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( AFRICA, 'https://www.torontozoo.com/!/pdfs/food/africa.pdf' ) ],
      [],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/!/pdfs/food/africa.pdf', AFRICA, 'Closed for the Season' ) ] ),
   )

   with pytest.raises( TypeError ):
      CHECKER.check_schedules( database, TODAY )
