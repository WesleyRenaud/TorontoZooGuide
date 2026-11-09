from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.gift_shop_list_checker import GiftShopListChecker as gift_shop_list_checker
from tools.checks.website_page import WebsitePage


ZOOTIQUE = 'Zootique'
KIOSK = 'Savanna Shop'
OUTPOST = 'Eurasia Wilds Outpost'
TODAY = date( 2026, 11, 3 )
SCHEMA = """
CREATE TABLE GiftShop (
   NAME TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);
"""


def _write_database( path: Path, gift_shops: list[ str ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO GiftShop ( NAME ) VALUES ( ? )',
      [ ( name, ) for name in gift_shops ],
   )
   connection.commit()
   connection.close()


def _page(
      titles: list[ str ],
      commented: list[ str ] | None = None ) -> str:
   hidden = [] if commented == None else commented
   parts = [ '<p><strong>Explore the Online Zoo Shop</strong></p>' ]

   for title in titles:
      parts.append(
         f'<div class="col3">'
         f'<strong>{ title }</strong>'
         f'<span class="opentxt">Open Daily</span>'
         f'<strong>(Hours subject to change)</strong>'
         f'</div>'
      )

   for title in hidden:
      parts.append(
         f'<!--div class="col3">'
         f'<strong>{ title }</strong>'
         f'<span class="opentxt">Closed for the Season</span>'
         f'</div-->'
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
   result = gift_shop_list_checker.check_lists( database, today )
   return result, capsys.readouterr().out


def Test_CheckLists_TestWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE ] )
   _install_page( monkeypatch, _page( [ ZOOTIQUE, 'Discovery Zone' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output
   assert '  Discovery Zone' in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output
   assert 'Online Zoo Shop' not in output
   assert 'Hours subject to change' not in output


def Test_CheckLists_TestAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE, KIOSK ] )
   _install_page( monkeypatch, _page( [ ZOOTIQUE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
   assert f'  { KIOSK }' in output
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output


def Test_CheckLists_TestNormalizedNames_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ZOOTIQUE,
         'Savanna Shop',
         "Wolf's Den Shop",
         'Twiga Market (Giraffe)',
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         'zootique',
         'Savanna-Shop',
         'Wolf’s Den Shop',
         'Twiga Market',
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


def Test_CheckLists_TestCommentedShop_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE, KIOSK ] )
   _install_page(
      monkeypatch,
      _page( [ ZOOTIQUE ], commented=[ KIOSK, 'Tundra Trading Post' ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { KIOSK }' in output
   assert 'Tundra Trading Post' not in output
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output


def Test_CheckLists_TestBothSides_ExpectIssueCount(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE, KIOSK ] )
   _install_page( monkeypatch, _page( [ ZOOTIQUE, 'Discovery Zone' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert output.startswith( f'Gift shop list check for { TODAY.isoformat() }.' )
   assert '  Discovery Zone' in output
   assert f'  { KIOSK }' in output


def Test_CheckLists_TestDuplicateCard_ExpectOneListing(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE ] )
   _install_page( monkeypatch, _page( [ 'Discovery Zone', 'Discovery Zone' ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
   assert output.count( '  Discovery Zone' ) == 1


def Test_CheckLists_TestWebsiteImage_ExpectWebPhoto(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE ] )
   _install_page(
      monkeypatch,
      _page( [ ZOOTIQUE ] )
      + (
         '<div class="col3">'
         '<img alt="" src="/!/img/pg/shops/discovery.jpg" />'
         '<strong>Discovery Zone</strong>'
         '<span class="opentxt">Open Daily</span>'
         '<strong>(Hours subject to change)</strong>'
         '</div>'
      ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'https://www.torontozoo.com/!/img/pg/shops/discovery.jpg' in output
   assert '  Discovery Zone' in output


def Test_CheckLists_TestAppPhoto_ExpectDetailImage(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ZOOTIQUE, OUTPOST ] )
   _install_page( monkeypatch, _page( [ ZOOTIQUE ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'images/details/gift-shops/eurasia-wilds-outpost.png' in output
   assert f'  { OUTPOST } · Eurasia Wilds' in output
