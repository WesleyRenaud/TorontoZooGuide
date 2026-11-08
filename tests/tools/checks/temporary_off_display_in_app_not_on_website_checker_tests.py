from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.app_string_provider import AppStringProvider
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.temporary_off_display_in_app_not_on_website_checker import TemporaryOffDisplayInAppNotOnWebsiteChecker as CHECKER
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 8 )
YESTERDAY = '2026-11-07'
STILL_OFF = '2026-11-20'
GORILLA = 'Western Lowland Gorilla'
ORANGUTAN = 'Sumatran Orangutan'
PYTHON = 'Reticulated Python'
BONYTONGUE = 'Malayan Bonytongue'
BARB = 'Red-Lined Torpedo Barb'
BETTONG = 'Brush-Tailed Bettong'
STORK = 'Marabou Stork'
TAPIR = 'Malayan Tapir'
RAINFOREST = 'African Rainforest Pavilion'
INDO_MALAYA = 'Indo-Malaya Pavilion'
AUSTRALASIA = 'Australasia Pavilion'
AFRICA = 'Africa Savanna'
CLOSURE = 'Indoor Orangutan Habitat Closure'
CLOSURE_START = '2026-05-13'
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
"""


def _database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   rows = (
      ( GORILLA, RAINFOREST, 'Habitat', '2026-11-01', STILL_OFF, 0, None, None ),
      ( ORANGUTAN, INDO_MALAYA, 'Indoor', '2026-05-13', STILL_OFF, 0, CLOSURE, CLOSURE_START ),
      ( PYTHON, INDO_MALAYA, 'Reptiles', '2026-05-13', STILL_OFF, 0, CLOSURE, CLOSURE_START ),
      ( BONYTONGUE, INDO_MALAYA, 'Aquarium', '2026-05-13', STILL_OFF, 0, CLOSURE, CLOSURE_START ),
      ( BARB, INDO_MALAYA, 'Stream', '2026-05-13', STILL_OFF, 0, CLOSURE, CLOSURE_START ),
      ( BETTONG, AUSTRALASIA, 'Outdoor', '2026-11-08', '2026-11-15', 0, None, None ),
      ( STORK, AFRICA, 'Savanna', '2026-11-01', '2026-11-30', 1, None, None ),
      ( TAPIR, INDO_MALAYA, 'Habitat', '2026-11-01', YESTERDAY, 0, None, None ),
   )

   for row in rows:
      connection.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES, EXHIBIT, IS_OFF_DISPLAY, VIEWING_SCOPE, OFF_DISPLAY_MESSAGE,
                  OFF_DISPLAY_START, OFF_DISPLAY_END, OFF_DISPLAY_FOR_SEASON,
                  CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
               ) VALUES ( ?, ?, 1, ?, '', ?, ?, ?, ?, ? )
         """,
         row,
      )

   connection.commit()
   connection.close()


def _page( names_by_section: dict[ str, list[ str ] ] ) -> str:
   blocks = []

   for section, names in names_by_section.items():
      cards = []

      for name in names:
         href = name.replace( ' ', '%20' )
         cards.append(
            f'<a href="/animals/{ href }">'
            '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
            '</a>'
         )

      blocks.append(
         f'<div class="atitle scrolling-title" id="{ section }">'
         + ''.join( cards )
         + '</div>'
      )

   return ''.join( blocks )


def _install_page(
      monkeypatch: pytest.MonkeyPatch,
      names_by_section: dict[ str, list[ str ] ] ) -> None:
   def fetch_text( url: str ) -> str:
      return _page( names_by_section )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _line( species: str, exhibit: str ) -> str:
   return '\n'.join( [
      CheckReport.text( 'checks.categoryItem' )
      + AppStringProvider.format( 'format.middleDotPair', first=species, second=exhibit ),
      CheckReport.detail_item(
         CheckReport.text( 'checks.photo' )
         + AnimalDetailImage.source( exhibit, species )
      ),
      CheckReport.detail_item( CheckReport.text( 'checks.setOnDisplay' ) ),
   ] )


def _species( path: Path ) -> list[ str ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      'SELECT SPECIES FROM AnimalStatus ORDER BY SPECIES'
   ).fetchall()
   connection.close()
   return [ row[ 0 ] for row in rows ]


def Test_CheckSchedules_TestClosureStillOnWebsite_ExpectOrangutanStays(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   _install_page( monkeypatch, {
      INDO_MALAYA: [ PYTHON, BONYTONGUE, BARB ],
      AUSTRALASIA: [ BETTONG ],
   } )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert _species( database ) == [
      BETTONG,
      BONYTONGUE,
      TAPIR,
      STORK,
      BARB,
      PYTHON,
      ORANGUTAN,
   ]
   assert capsys.readouterr().out == (
      CheckReport.heading( 'temporaryOffDisplay', TODAY )
      + '\n\n'
      + CheckReport.category_line( 'checks.temporaryOffDisplayAppOnly', 1 )
      + '\n'
      + _line( GORILLA, RAINFOREST )
      + '\n\n'
   )


def Test_CheckSchedules_TestClosureAnimalsBackOnWebsite_ExpectOrangutanOnDisplay(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   _install_page( monkeypatch, {
      AUSTRALASIA: [ BETTONG ],
   } )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 5
   assert _species( database ) == [ BETTONG, TAPIR, STORK ]
   assert capsys.readouterr().out == (
      CheckReport.heading( 'temporaryOffDisplay', TODAY )
      + '\n\n'
      + CheckReport.category_line( 'checks.temporaryOffDisplayAppOnly', 5 )
      + '\n'
      + _line( BONYTONGUE, INDO_MALAYA )
      + '\n'
      + _line( BARB, INDO_MALAYA )
      + '\n'
      + _line( PYTHON, INDO_MALAYA )
      + '\n'
      + _line( ORANGUTAN, INDO_MALAYA )
      + '\n'
      + _line( GORILLA, RAINFOREST )
      + '\n\n'
   )
