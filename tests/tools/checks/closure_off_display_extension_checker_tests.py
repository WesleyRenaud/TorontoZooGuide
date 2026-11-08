from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.closure_off_display_extension_checker import ClosureOffDisplayExtensionChecker as CHECKER
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 8 )
LAST_DAY = '2026-11-08'
LATER = '2026-11-12'
EXTENDED = date( 2026, 11, 15 )
EXHIBIT = 'Indo-Malaya Pavilion'
ORANGUTAN = 'Sumatran Orangutan'
GIBBON = 'White-Handed Gibbon'
TAPIR = 'Malayan Tapir'
PANDA = 'Red Panda'
SEASONAL = 'Binturong'
ORANGUTAN_UPDATE = 'Indoor Orangutan Habitat Closure'
ORANGUTAN_START = '2026-05-13'
EURASIA_UPDATE = 'Eurasia Loop Partial Closure'
EURASIA_START = '2026-05-03'
SCHEMA = """
CREATE TABLE AnimalStatus (
   SPECIES                 TEXT NOT NULL,
   EXHIBIT                 TEXT NOT NULL,
   IS_OFF_DISPLAY          BOOL NOT NULL,
   VIEWING_SCOPE           TEXT NOT NULL,
   OFF_DISPLAY_MESSAGE     TEXT,
   OFF_DISPLAY_START       DATE,
   OFF_DISPLAY_END         DATE,
   OFF_DISPLAY_FOR_SEASON  BOOL NOT NULL,
   CLOSURE_UPDATE_TITLE    TEXT,
   CLOSURE_UPDATE_START    DATE,
   PRIMARY KEY ( SPECIES, EXHIBIT, VIEWING_SCOPE )
);

CREATE TABLE ZooUpdate (
   TITLE          TEXT NOT NULL,
   DESCRIPTION    TEXT,
   UPDATE_TYPE    TEXT,
   START_DATE     DATE NOT NULL,
   END_DATE       DATE,
   PRIMARY KEY ( TITLE, START_DATE )
);
"""


def _database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.execute(
      """   INSERT INTO ZooUpdate ( TITLE, DESCRIPTION, UPDATE_TYPE, START_DATE, END_DATE )
            VALUES ( ?, '', 'Closure', ?, ? )
      """,
      ( ORANGUTAN_UPDATE, ORANGUTAN_START, LAST_DAY ),
   )
   connection.execute(
      """   INSERT INTO ZooUpdate ( TITLE, DESCRIPTION, UPDATE_TYPE, START_DATE, END_DATE )
            VALUES ( ?, '', 'Closure', ?, NULL )
      """,
      ( EURASIA_UPDATE, EURASIA_START ),
   )
   rows = (
      ( ORANGUTAN, EXHIBIT, 1, 'Indoor habitat', LAST_DAY, 0, ORANGUTAN_UPDATE, ORANGUTAN_START ),
      ( ORANGUTAN, EXHIBIT, 1, 'Outdoor habitat', LAST_DAY, 0, ORANGUTAN_UPDATE, ORANGUTAN_START ),
      ( GIBBON, EXHIBIT, 1, 'Gibbon habitat', LATER, 0, ORANGUTAN_UPDATE, ORANGUTAN_START ),
      ( TAPIR, EXHIBIT, 0, 'Tapir habitat', LAST_DAY, 0, ORANGUTAN_UPDATE, ORANGUTAN_START ),
      ( SEASONAL, EXHIBIT, 1, 'Seasonal habitat', LAST_DAY, 1, ORANGUTAN_UPDATE, ORANGUTAN_START ),
      ( PANDA, 'Eurasia Wilds', 1, 'Panda habitat', LAST_DAY, 0, EURASIA_UPDATE, EURASIA_START ),
   )

   for species, exhibit, off_display, scope, end, for_season, title, start in rows:
      connection.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  VIEWING_SCOPE,
                  OFF_DISPLAY_MESSAGE,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_FOR_SEASON,
                  CLOSURE_UPDATE_TITLE,
                  CLOSURE_UPDATE_START
               ) VALUES ( ?, ?, ?, ?, '', ?, ?, ?, ?, ? )
         """,
         ( species, exhibit, off_display, scope, ORANGUTAN_START, end, for_season, title, start ),
      )

   connection.commit()
   connection.close()


def _page( names: list[ str ] ) -> str:
   cards = []

   for name in names:
      href = name.replace( ' ', '%20' )
      cards.append(
         f'<a href="/animals/{ href }">'
         '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
         '</a>'
      )

   cards.append(
      '<a href="/animals/Marabou%20Stork">'
      '<span class="line2 status sseason">Off for the Season</span>'
      '</a>'
   )
   return (
      '<div class="atitle scrolling-title" id="Indo-Malaya">'
      + ''.join( cards )
      + '</div>'
   )


def _install_page( monkeypatch: pytest.MonkeyPatch, names: list[ str ] ) -> None:
   def fetch_text( url: str ) -> str:
      return _page( names )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _line( species: str, exhibit: str ) -> str:
   lines = [
      CheckReport.text( 'checks.categoryItem' )
      + AppStringProvider.format( 'format.middleDotPair', first=species, second=exhibit )
   ]
   lines.append( CheckReport.detail_item(
      CheckReport.text( 'checks.photo' )
      + AnimalDetailImage.source( exhibit, species )
   ) )
   lines.append( CheckReport.detail_item(
      CheckReport.text( 'checks.extendedOffDisplayThrough' )
      + DateValues.format_display_date_value( EXTENDED )
      + CheckReport.text( 'checks.period' )
   ) )
   return '\n'.join( lines )


def _ends( path: Path ) -> dict[ tuple[ str, str ], str | None ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      """   SELECT SPECIES, VIEWING_SCOPE, OFF_DISPLAY_END
            FROM AnimalStatus
      """
   ).fetchall()
   connection.close()
   return {
      ( species, scope ): end
      for species, scope, end in rows
   }


def _update_end( path: Path, title: str ) -> str | None:
   connection = sqlite3.connect( path )
   row = connection.execute(
      'SELECT END_DATE FROM ZooUpdate WHERE TITLE = ?',
      ( title, ),
   ).fetchone()
   connection.close()
   return row[ 0 ]


def Test_CheckSchedules_TestLinkedAnimalReturnsTomorrow_ExpectClosureExtended(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   _install_page( monkeypatch, [ ORANGUTAN, GIBBON, TAPIR ] )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )
   output = capsys.readouterr().out

   assert result == 0
   assert CheckReport.fixed_count == 2
   assert _update_end( database, ORANGUTAN_UPDATE ) == EXTENDED.isoformat()
   assert _update_end( database, EURASIA_UPDATE ) == None
   ends = _ends( database )
   assert ends[ ( ORANGUTAN, 'Indoor habitat' ) ] == EXTENDED.isoformat()
   assert ends[ ( ORANGUTAN, 'Outdoor habitat' ) ] == EXTENDED.isoformat()
   assert ends[ ( GIBBON, 'Gibbon habitat' ) ] == EXTENDED.isoformat()
   assert ends[ ( TAPIR, 'Tapir habitat' ) ] == LAST_DAY
   assert ends[ ( SEASONAL, 'Seasonal habitat' ) ] == LAST_DAY
   assert ends[ ( PANDA, 'Panda habitat' ) ] == LAST_DAY
   assert output == (
      CheckReport.heading( 'closureOffDisplay', TODAY )
      + '\n\n'
      + CheckReport.category_line( 'checks.closureOffDisplayReturningTomorrow', 2 )
      + '\n'
      + _line( ORANGUTAN, EXHIBIT )
      + '\n'
      + _line( GIBBON, EXHIBIT )
      + '\n\n'
   )


def Test_CheckSchedules_TestReturningTomorrowNotOnWebsite_ExpectUnchanged(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   _install_page( monkeypatch, [ TAPIR ] )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert capsys.readouterr().out == ''
   assert _update_end( database, ORANGUTAN_UPDATE ) == LAST_DAY
   assert _ends( database )[ ( ORANGUTAN, 'Indoor habitat' ) ] == LAST_DAY
   assert _ends( database )[ ( GIBBON, 'Gibbon habitat' ) ] == LATER


def Test_CheckSchedules_TestNoAnimalReturnsTomorrow_ExpectUnchanged(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   connection = sqlite3.connect( database )
   connection.execute(
      """   UPDATE AnimalStatus
            SET OFF_DISPLAY_END = ?
            WHERE OFF_DISPLAY_END = ?
               AND OFF_DISPLAY_FOR_SEASON = 0
      """,
      ( LATER, LAST_DAY ),
   )
   connection.execute(
      'UPDATE ZooUpdate SET END_DATE = ? WHERE TITLE = ?',
      ( LATER, ORANGUTAN_UPDATE ),
   )
   connection.commit()
   connection.close()
   _install_page( monkeypatch, [ ORANGUTAN, GIBBON, PANDA ] )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert capsys.readouterr().out == ''
   assert _ends( database )[ ( GIBBON, 'Gibbon habitat' ) ] == LATER
   assert _update_end( database, ORANGUTAN_UPDATE ) == LATER
