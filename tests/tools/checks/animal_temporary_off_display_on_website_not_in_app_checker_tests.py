from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.animal_temporary_off_display_on_website_not_in_app_checker import AnimalTemporaryOffDisplayOnWebsiteNotInAppChecker as CHECKER
from tools.checks.check_report import CheckReport
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 8 )
LAST_DAY = date( 2026, 11, 15 )
YESTERDAY = '2026-11-07'
STILL_OFF = '2026-11-20'
BETTONG = 'Brush-tailed Bettong'
COCKATOO = 'Red-tailed Black Cockatoo'
ORANGUTAN = 'Sumatran Orangutan'
STORK = 'Marabou Stork'
UNKNOWN = 'Mystery Animal'
AUSTRALASIA = 'Australasia Pavilion'
INDO_MALAYA = 'Indo-Malaya Pavilion'
AFRICA = 'Africa Savanna'
CLOSURE = 'Indoor Orangutan Habitat Closure'
CLOSURE_START = '2026-05-13'
SCHEMA = """
CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL
);

CREATE TABLE EnclosureViewing (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   NAME TEXT NOT NULL
);

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
   enclosures = (
      ( BETTONG, AUSTRALASIA, 'Outdoor' ),
      ( COCKATOO, AUSTRALASIA, 'Aviary' ),
      ( ORANGUTAN, INDO_MALAYA, 'Indoor' ),
      ( STORK, AFRICA, 'Savanna' ),
   )

   for species, exhibit, scope in enclosures:
      connection.execute(
         'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? )',
         ( species, exhibit ),
      )
      connection.execute(
         'INSERT INTO EnclosureViewing ( SPECIES, EXHIBIT, NAME ) VALUES ( ?, ?, ? )',
         ( species, exhibit, scope ),
      )

   connection.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, IS_OFF_DISPLAY, VIEWING_SCOPE, OFF_DISPLAY_MESSAGE,
               OFF_DISPLAY_START, OFF_DISPLAY_END, OFF_DISPLAY_FOR_SEASON,
               CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            ) VALUES ( ?, ?, 1, 'Aviary', '', ?, ?, 0, ?, ? )
      """,
      ( COCKATOO, AUSTRALASIA, '2026-11-01', YESTERDAY, CLOSURE, CLOSURE_START ),
   )
   connection.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, IS_OFF_DISPLAY, VIEWING_SCOPE, OFF_DISPLAY_MESSAGE,
               OFF_DISPLAY_START, OFF_DISPLAY_END, OFF_DISPLAY_FOR_SEASON,
               CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            ) VALUES ( ?, ?, 1, 'Indoor', '', '2026-05-13', ?, 0, ?, ? )
      """,
      ( ORANGUTAN, INDO_MALAYA, STILL_OFF, CLOSURE, CLOSURE_START ),
   )
   connection.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, IS_OFF_DISPLAY, VIEWING_SCOPE, OFF_DISPLAY_MESSAGE,
               OFF_DISPLAY_START, OFF_DISPLAY_END, OFF_DISPLAY_FOR_SEASON,
               CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            ) VALUES ( ?, ?, 1, 'Savanna', '', '2026-11-01', '2026-11-30', 1, NULL, NULL )
      """,
      ( STORK, AFRICA ),
   )
   connection.commit()
   connection.close()


def _page() -> str:
   sections = {
      AUSTRALASIA: [ BETTONG, COCKATOO ],
      INDO_MALAYA: [ ORANGUTAN ],
      AFRICA: [ STORK, UNKNOWN ],
   }
   blocks = []

   for section, names in sections.items():
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


def _install_page( monkeypatch: pytest.MonkeyPatch ) -> None:
   def fetch_text( url: str ) -> str:
      return _page()

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
      CheckReport.text( 'checks.setOffDisplayThrough' )
      + DateValues.format_display_date_value( LAST_DAY )
      + CheckReport.text( 'checks.period' )
   ) )
   return '\n'.join( lines )


def _statuses( path: Path ) -> list[ tuple ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      """   SELECT
               SPECIES,
               OFF_DISPLAY_START,
               OFF_DISPLAY_END,
               OFF_DISPLAY_FOR_SEASON,
               CLOSURE_UPDATE_TITLE
            FROM AnimalStatus
            ORDER BY SPECIES
      """
   ).fetchall()
   connection.close()
   return rows


def Test_CheckSchedules_TestWebsiteOnlyTemporary_ExpectOffDisplayForOneWeek(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )
   _install_page( monkeypatch )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 1
   assert CheckReport.fixed_count == 2
   assert _statuses( database ) == [
      ( BETTONG, TODAY.isoformat(), LAST_DAY.isoformat(), 0, None ),
      ( STORK, '2026-11-01', '2026-11-30', 1, None ),
      ( COCKATOO, TODAY.isoformat(), LAST_DAY.isoformat(), 0, None ),
      ( ORANGUTAN, '2026-05-13', STILL_OFF, 0, CLOSURE ),
   ]
   assert capsys.readouterr().out == (
      CheckReport.heading( 'temporaryOffDisplay', TODAY )
      + '\n\n'
      + CheckReport.category_line( 'checks.temporaryOffDisplayWebsiteOnly', 3 )
      + '\n'
      + _line( BETTONG, AUSTRALASIA )
      + '\n'
      + CheckReport.text( 'checks.categoryItem' )
      + UNKNOWN
      + '\n'
      + _line( COCKATOO, AUSTRALASIA )
      + '\n\n'
   )


def Test_CheckSchedules_TestAlreadyOffDisplay_ExpectUnchanged(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'
   _database( database )

   def fetch_text( url: str ) -> str:
      return (
         '<div class="atitle scrolling-title" id="Indo-Malaya Pavilion">'
         '<a href="/animals/Sumatran%20Orangutan">'
         '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
         '</a>'
         '</div>'
      )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )
   CheckReport.reset_fixed_count()

   result = CHECKER.check_schedules( database, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert capsys.readouterr().out == ''
   statuses = _statuses( database )
   assert len( statuses ) == 3
   assert ( ORANGUTAN, '2026-05-13', STILL_OFF, 0, CLOSURE ) in statuses
