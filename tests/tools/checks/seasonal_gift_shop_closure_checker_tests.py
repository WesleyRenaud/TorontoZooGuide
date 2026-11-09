from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.seasonal_gift_shop_closure_checker import SeasonalGiftShopClosureChecker as CHECKER
from tools.checks.website_page import WebsitePage


ZOOTIQUE = 'Zootique'
KIOSK = 'Savanna Shop'
OUTPOST = 'Eurasia Wilds Outpost'
TODAY = date( 2026, 11, 2 )
RAMP_UP = date( 2026, 3, 15 )
STEADY = date( 2026, 7, 15 )
APRIL = date( 2027, 4, 30 )
UNTIL_MONTHS = {
   KIOSK: 3,
   OUTPOST: 3,
}
SCHEMA = """
CREATE TABLE GiftShop (
   NAME TEXT NOT NULL,
   CLOSED_FOR_SEASON_UNTIL_MONTH INTEGER,
   PRIMARY KEY ( NAME )
);

CREATE TABLE GiftShopStatus (
   GIFT_SHOP          TEXT NOT NULL PRIMARY KEY,
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




def _write_database(
      path: Path,
      gift_shops: list[ str ],
      closed_for_season: list[ tuple[ str, str | None, str | None ] ],
      curves: list[ tuple[ date, float, float ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO GiftShop ( NAME, CLOSED_FOR_SEASON_UNTIL_MONTH ) VALUES ( ?, ? )',
      [
         ( name, UNTIL_MONTHS.get( name ) )
         for name in gift_shops
      ],
   )

   for name, start, end in closed_for_season:
      connection.execute(
         """   INSERT INTO GiftShopStatus (
                  GIFT_SHOP,
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
         ( ZOOTIQUE, 'Africa', yesterday.month, yesterday.day, yesterday_value ),
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
         ( ZOOTIQUE, 'Africa', scheduled_date.month, scheduled_date.day, today_value ),
      )

   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str, str ] ] ) -> str:
   parts = []

   for href, title, status in cards:
      hours = '<strong>(Hours subject to change)</strong>'
      body = (
         f'<strong>{ title }</strong>'
         f'<span class="opentxt">{ status }</span>'
         f'{ hours }'
      )

      if href == '':
         parts.append( f'<div class="col3">{ body }</div>' )
         continue

      parts.append( f'<a class="col3" href="{ href }">{ body }</a>' )

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
            FROM GiftShopStatus
            WHERE GIFT_SHOP = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()

   if row == None:
      return None

   return ( row[ 0 ], row[ 1 ], row[ 2 ], row[ 3 ] )


def Test_CheckSchedules_TestRampDownWebsiteOnly_ExpectClosedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', 'Savanna shop', 'Closed For The Season' ),
         ( '', ZOOTIQUE, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { KIOSK }' in output
   assert 'images/details/gift-shops/savanna-shop.png' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert 'March 31, 2027' in output
   assert _season_row( database, KIOSK ) == ( 1, TODAY.isoformat(), '2027-03-31', 1 )
   assert ZOOTIQUE not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestCardWithoutLink_ExpectUnmatchedReported(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK ],
      [ ( KIOSK, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', KIOSK, 'Closed for the Season' ),
         ( '/retail/discovery', 'Discovery Zone', 'Closed for the Season' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert KIOSK not in output
   assert '  Discovery Zone' in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestCommentedClosedCard_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK, ZOOTIQUE ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      (
         '<div class="col3">'
         f'<strong>{ ZOOTIQUE }</strong>'
         '<span class="opentxt">Open Daily</span>'
         '</div>'
         '<!--hr />'
         '<div class="col3">'
         f'<strong>{ KIOSK }</strong>'
         '<span class="opentxt">Closed for the Season</span>'
         '</div-->'
      ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert KIOSK not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestUnknownWebsiteCard_ExpectReported(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ZOOTIQUE ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', 'Discovery Zone', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert '  Discovery Zone' in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output


def Test_CheckSchedules_TestRampDownAppOnly_ExpectOpenedAndClosed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   ended = TODAY - timedelta( days=1 )
   _write_database(
      database,
      [ KIOSK, OUTPOST, ZOOTIQUE ],
      [
         ( OUTPOST, TODAY.isoformat(), None ),
         ( ZOOTIQUE, None, ended.isoformat() ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', KIOSK, 'Closed For The Season' ),
         ( '', ZOOTIQUE, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { KIOSK }' in output
   assert f'  { OUTPOST }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, KIOSK ) == ( 1, TODAY.isoformat(), '2027-03-31', 1 )
   assert _season_row( database, OUTPOST ) == None
   assert ZOOTIQUE not in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestOpenThroughPastDate_ExpectWebsiteSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK ],
      [ ( KIOSK, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', KIOSK, 'Open Weekends Through October 31st' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert KIOSK not in output
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
      [ KIOSK ],
      [ ( KIOSK, through_today.isoformat(), None ) ],
      [ ( through_today, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '', KIOSK, 'Open Weekends Through October 31' ),
      ] ),
   )

   result, output = _check( database, through_today, capsys )

   assert result == 0
   assert f'  { KIOSK }' in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, KIOSK ) == None
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK ],
      [ ( KIOSK, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', 'Savanna shop', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestDifferentGiftShopsClosed_ExpectBothCorrected(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK, ZOOTIQUE ],
      [ ( KIOSK, RAMP_UP.isoformat(), None ) ],
      [ ( RAMP_UP, 0.5, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', ZOOTIQUE, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, RAMP_UP, capsys )

   assert result == 0
   assert f'  { KIOSK }' in output
   assert f'  { ZOOTIQUE } · Front Courtyard' in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert CheckReport.text( 'checks.extendedClosedForSeasonThrough' ) in output
   assert 'March 22, 2026' in output
   assert _season_row( database, KIOSK ) == None
   assert _season_row( database, ZOOTIQUE ) == ( 1, RAMP_UP.isoformat(), '2026-03-22', 1 )
   assert CheckReport.category_line( 'checks.closedForSeasonReturningSoon', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestClosedOnSteadyDate_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ KIOSK ],
      [ ( KIOSK, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', KIOSK, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert KIOSK not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestSeasonEndToday_ExpectExtendedOneWeek(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   start = '2026-11-08'
   _write_database(
      database,
      [ KIOSK ],
      [ ( KIOSK, start, APRIL.isoformat() ) ],
      [ ( APRIL, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', KIOSK, 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, APRIL, capsys )

   assert result == 0
   assert CheckReport.text( 'checks.extendedClosedForSeasonThrough' ) in output
   assert 'May 8, 2027' in output
   assert _season_row( database, KIOSK ) == ( 1, start, '2027-05-08', 1 )


def Test_CheckSchedules_TestNoUntilMonth_ExpectCrash(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ZOOTIQUE ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '', ZOOTIQUE, 'Closed for the Season' ) ] ),
   )

   with pytest.raises( TypeError ):
      CHECKER.check_schedules( database, TODAY )
