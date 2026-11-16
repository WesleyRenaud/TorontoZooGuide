from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.shared.enums.item_type import ItemType
from tools.checks.attraction_temporary_closure_checker import AttractionTemporaryClosureChecker
from tools.checks.check_report import CheckReport
from tools.checks.gift_shop_temporary_closure_checker import GiftShopTemporaryClosureChecker
from tools.checks.restaurant_temporary_closure_checker import RestaurantTemporaryClosureChecker
from tools.checks.temporary_closure_reader import TemporaryClosureReader
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 15 )
NAMES = {
   ItemType.ATTRACTION: [ 'Splash Island', 'Waterside Theatre' ],
   ItemType.RESTAURANT: [ 'Caribou Café' ],
   ItemType.GIFT_SHOP: [ 'Zootique' ],
}
TABLES = {
   ItemType.ATTRACTION: ( 'AttractionScheduleOverride', 'ATTRACTION' ),
   ItemType.RESTAURANT: ( 'RestaurantScheduleOverride', 'RESTAURANT' ),
   ItemType.GIFT_SHOP: ( 'GiftShopScheduleOverride', 'GIFT_SHOP' ),
}
SCHEMA = """
CREATE TABLE Attraction ( NAME TEXT PRIMARY KEY );
CREATE TABLE Restaurant ( NAME TEXT PRIMARY KEY );
CREATE TABLE GiftShop ( NAME TEXT PRIMARY KEY );

CREATE TABLE AttractionScheduleOverride (
   ATTRACTION TEXT NOT NULL,
   OVERRIDE_START_DATE TEXT NOT NULL,
   OVERRIDE_END_DATE TEXT,
   IS_CLOSED INTEGER NOT NULL,
   OVERRIDE_MESSAGE TEXT,
   PRIMARY KEY ( ATTRACTION, OVERRIDE_START_DATE )
);

CREATE TABLE RestaurantScheduleOverride (
   RESTAURANT TEXT NOT NULL,
   OVERRIDE_START_DATE TEXT NOT NULL,
   OVERRIDE_END_DATE TEXT,
   IS_CLOSED INTEGER NOT NULL,
   OVERRIDE_MESSAGE TEXT,
   PRIMARY KEY ( RESTAURANT, OVERRIDE_START_DATE )
);

CREATE TABLE GiftShopScheduleOverride (
   GIFT_SHOP TEXT NOT NULL,
   OVERRIDE_START_DATE TEXT NOT NULL,
   OVERRIDE_END_DATE TEXT,
   IS_CLOSED INTEGER NOT NULL,
   OVERRIDE_MESSAGE TEXT,
   PRIMARY KEY ( GIFT_SHOP, OVERRIDE_START_DATE )
);
"""


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def box( title: str, description: str ) -> str:
   return f'<p><strong>{ title }</strong> { description }</p>'


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Attraction ( NAME ) VALUES ( ? )',
      [ ( 'Splash Island', ), ( 'Waterside Theatre', ) ],
   )
   connection.execute( 'INSERT INTO Restaurant ( NAME ) VALUES ( ? )', ( 'Caribou Café', ) )
   connection.execute( 'INSERT INTO GiftShop ( NAME ) VALUES ( ? )', ( 'Zootique', ) )
   connection.commit()
   connection.close()


def insert_override(
      path: Path,
      kind: ItemType,
      place: str,
      message: str,
      start: str,
      end: str | None ) -> None:
   table, column = TABLES[ kind ]
   connection = sqlite3.connect( path )
   connection.execute(
      f"""   INSERT INTO { table } (
               { column },
               OVERRIDE_START_DATE,
               OVERRIDE_END_DATE,
               IS_CLOSED,
               OVERRIDE_MESSAGE
            ) VALUES ( ?, ?, ?, 1, ? )
      """,
      ( place, start, end, message ),
   )
   connection.commit()
   connection.close()


def overrides( path: Path ) -> list[ tuple[ str, str, str | None, int, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = []

   for table, column in TABLES.values():
      loaded.extend(
         connection.execute(
            f"""   SELECT
                     { column },
                     OVERRIDE_START_DATE,
                     OVERRIDE_END_DATE,
                     IS_CLOSED,
                     OVERRIDE_MESSAGE
                  FROM { table }
            """
         )
      )

   connection.close()
   return [ tuple( row ) for row in loaded ]


def notice( html: str, place: str ) -> str:
   for kind, names in NAMES.items():
      if place not in names:
         continue

      for item in TemporaryClosureReader.read( html, { name: name for name in names }, kind ):
         if item.place == place:
            return item.message

   raise AssertionError( place )


def check(
      path: Path,
      html: str,
      monkeypatch: pytest.MonkeyPatch,
      checker: (
         type[ AttractionTemporaryClosureChecker ]
         | type[ RestaurantTemporaryClosureChecker ]
         | type[ GiftShopTemporaryClosureChecker ]
      ) ) -> int:
   monkeypatch.setattr( WebsitePage, 'fetch_text', lambda url: html )
   CheckReport.reset_fixed_count()
   return checker.check_schedules( path, TODAY )


def Test_CheckSchedules_TestNewNotice_ExpectMonthWindow(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box( 'Maintenance', 'Splash Island is closed for repairs.' ),
   ] )

   result = check( database_path, html, monkeypatch, AttractionTemporaryClosureChecker )
   output = capsys.readouterr().out

   assert result == 0
   assert 'Photo: images/details/attractions/splash-island.png' in output
   assert overrides( database_path ) == [
      (
         'Splash Island',
         '2026-11-15',
         '2026-12-15',
         1,
         notice( html, 'Splash Island' ),
      ),
   ]


def Test_CheckSchedules_TestMissingNotice_ExpectOpened(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_override(
      database_path,
      ItemType.RESTAURANT,
      'Caribou Café',
      'Caribou Café is closed for repairs.',
      '2026-11-01',
      '2026-12-01',
   )

   result = check(
      database_path,
      page( [] ),
      monkeypatch,
      RestaurantTemporaryClosureChecker,
   )
   output = capsys.readouterr().out

   assert result == 0
   assert 'Photo: images/details/restaurants/caribou-cafe.png' in output
   assert overrides( database_path ) == [
      (
         'Caribou Café',
         '2026-11-01',
         '2026-11-14',
         1,
         'Caribou Café is closed for repairs.',
      ),
   ]


def Test_CheckSchedules_TestShortWindow_ExpectExtended(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box( 'Maintenance', 'Zootique is closed for repairs.' ),
   ] )
   message = notice( html, 'Zootique' )
   insert_override(
      database_path,
      ItemType.GIFT_SHOP,
      'Zootique',
      message,
      '2026-11-01',
      '2026-11-20',
   )

   result = check( database_path, html, monkeypatch, GiftShopTemporaryClosureChecker )
   output = capsys.readouterr().out

   assert result == 0
   assert 'Photo: images/details/gift-shops/zootique.png' in output
   assert overrides( database_path ) == [
      ( 'Zootique', '2026-11-01', '2026-12-15', 1, message ),
   ]


def Test_CheckSchedules_TestChangedSentence_ExpectNewClosure(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box( 'Maintenance', 'Waterside Theatre is closed for a show change.' ),
   ] )
   insert_override(
      database_path,
      ItemType.ATTRACTION,
      'Waterside Theatre',
      'Waterside Theatre is closed for repairs.',
      '2026-11-01',
      '2026-12-15',
   )

   result = check( database_path, html, monkeypatch, AttractionTemporaryClosureChecker )
   output = capsys.readouterr().out

   assert result == 0
   assert 'Photo: images/details/attractions/waterside-theatre.png' in output
   assert overrides( database_path ) == [
      (
         'Waterside Theatre',
         '2026-11-01',
         '2026-11-14',
         1,
         'Waterside Theatre is closed for repairs.',
      ),
      (
         'Waterside Theatre',
         '2026-11-15',
         '2026-12-15',
         1,
         notice( html, 'Waterside Theatre' ),
      ),
   ]


def Test_CheckSchedules_TestSeasonAndRestroom_ExpectNoClosure(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box( 'Season', 'Splash Island is closed for the season.' ),
      box( 'Washroom', 'The Splash Island washroom is closed for repairs.' ),
   ] )

   result = check( database_path, html, monkeypatch, AttractionTemporaryClosureChecker )

   assert result == 0
   assert overrides( database_path ) == []


def Test_CheckSchedules_TestEndPastHorizon_ExpectNoChange(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box( 'Maintenance', 'Zootique is closed for repairs.' ),
   ] )
   message = notice( html, 'Zootique' )
   insert_override(
      database_path,
      ItemType.GIFT_SHOP,
      'Zootique',
      message,
      '2026-11-01',
      '2026-12-20',
   )

   result = check( database_path, html, monkeypatch, GiftShopTemporaryClosureChecker )

   assert result == 0
   assert overrides( database_path ) == [
      ( 'Zootique', '2026-11-01', '2026-12-20', 1, message ),
   ]
