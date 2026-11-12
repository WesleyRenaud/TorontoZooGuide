from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.updates.domain.update_type import UpdateType
from tools.checks.check_report import CheckReport
from tools.checks.closure_update_checker import ClosureUpdateChecker
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 11 )
SCHEMA = """
CREATE TABLE ZooUpdate (
   TITLE TEXT NOT NULL,
   DESCRIPTION TEXT NOT NULL,
   UPDATE_TYPE TEXT NOT NULL,
   START_DATE TEXT NOT NULL,
   END_DATE TEXT,
   PRIMARY KEY (TITLE, START_DATE)
);

CREATE TABLE AnimalStatus (
   SPECIES TEXT,
   EXHIBIT TEXT,
   IS_OFF_DISPLAY INTEGER,
   OFF_DISPLAY_FOR_SEASON INTEGER,
   OFF_DISPLAY_END TEXT,
   CLOSURE_UPDATE_TITLE TEXT,
   CLOSURE_UPDATE_START TEXT
);
"""


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.commit()
   connection.close()


def insert_update(
      path: Path,
      title: str,
      description: str,
      update_type: str,
      start: str,
      end: str | None ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO ZooUpdate (
               TITLE, DESCRIPTION, UPDATE_TYPE, START_DATE, END_DATE
            ) VALUES (?, ?, ?, ?, ?)
      """,
      ( title, description, update_type, start, end ),
   )
   connection.commit()
   connection.close()


def insert_animal(
      path: Path,
      species: str,
      title: str,
      start: str ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, IS_OFF_DISPLAY, OFF_DISPLAY_FOR_SEASON,
               OFF_DISPLAY_END, CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            ) VALUES (?, ?, 1, 0, ?, ?, ?)
      """,
      ( species, 'Indo-Malaya Pavilion', '2026-11-20', title, start ),
   )
   connection.commit()
   connection.close()


def rows( path: Path ) -> list[ sqlite3.Row ]:
   connection = sqlite3.connect( path )
   connection.row_factory = sqlite3.Row
   loaded = connection.execute(
      """   SELECT TITLE, DESCRIPTION, UPDATE_TYPE, START_DATE, END_DATE
            FROM ZooUpdate
            ORDER BY TITLE, START_DATE
      """
   ).fetchall()
   connection.close()
   return loaded


def animals( path: Path ) -> list[ tuple[ str, str, str ] ]:
   connection = sqlite3.connect( path )
   loaded = connection.execute(
      """   SELECT SPECIES, CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            FROM AnimalStatus
            ORDER BY SPECIES
      """
   ).fetchall()
   connection.close()
   return loaded


def Test_CheckSchedules_TestNewClosure_ExpectMonthLongUpdate(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_update(
      database_path,
      'New Baby Camel!',
      'A calf was born.',
      UpdateType.ANIMAL_BIRTH.value,
      '2026-05-03',
      None,
   )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         '<p><strong>Please note that some outdoor animals may not be viewable.</strong></p>',
         '<p><strong>The polar bear underwater viewing area is closed for maintenance.</strong></p>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = ClosureUpdateChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert 'polar bear underwater viewing area is closed' in capsys.readouterr().out
   stored = {
      row[ 'TITLE' ]: ( row[ 'UPDATE_TYPE' ], row[ 'START_DATE' ], row[ 'END_DATE' ] )
      for row in rows( database_path )
   }
   assert stored[ 'New Baby Camel!' ] == ( 'Animal Birth', '2026-05-03', None )
   assert stored[
      'The polar bear underwater viewing area is closed for maintenance.'
   ] == ( 'Closure', '2026-11-11', '2026-12-11' )


def Test_CheckSchedules_TestMatchingEnds_ExpectMonthWithoutCuttingLonger(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_update(
      database_path,
      'Pathway is closed.',
      '',
      UpdateType.CLOSURE.value,
      '2026-05-03',
      '2026-11-20',
   )
   insert_update(
      database_path,
      'Pavilion is closed.',
      '',
      UpdateType.CLOSURE.value,
      '2026-05-01',
      '2027-06-01',
   )
   insert_update(
      database_path,
      'Trail is closed.',
      '',
      UpdateType.CLOSURE.value,
      '2026-05-02',
      None,
   )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         '<p><strong>Pathway is closed.</strong></p>',
         '<p><strong>Pavilion is closed.</strong></p>',
         '<p><strong>Trail is closed.</strong></p>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   ClosureUpdateChecker.check_schedules( database_path, TODAY )

   stored = {
      row[ 'TITLE' ]: ( row[ 'START_DATE' ], row[ 'END_DATE' ] )
      for row in rows( database_path )
   }
   assert stored[ 'Pathway is closed.' ] == ( '2026-05-03', '2026-12-11' )
   assert stored[ 'Pavilion is closed.' ] == ( '2026-05-01', '2027-06-01' )
   assert stored[ 'Trail is closed.' ] == ( '2026-05-02', None )


def Test_CheckSchedules_TestDifferentWording_ExpectReplacementAndMovedAnimal(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_update(
      database_path,
      'Indoor Orangutan Habitat Closure',
      'Old wording.',
      UpdateType.CLOSURE.value,
      '2026-05-13',
      '2026-11-20',
   )
   insert_update(
      database_path,
      'Gift shop path',
      'The shop path is closed.',
      UpdateType.CLOSURE.value,
      '2026-06-01',
      '2026-12-01',
   )
   insert_animal(
      database_path,
      'Sumatran orangutan',
      'Indoor Orangutan Habitat Closure',
      '2026-05-13',
   )
   insert_animal(
      database_path,
      'Fennec fox',
      'Gift shop path',
      '2026-06-01',
   )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         '<details><summary><strong>Indo-Malaya Pavilion Construction</strong></summary>'
         '<p>The Sumatran orangutan indoor habitat is closed due to construction.</p>'
         '</details>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   ClosureUpdateChecker.check_schedules( database_path, TODAY )

   stored = {
      ( row[ 'TITLE' ], row[ 'START_DATE' ] ): row[ 'END_DATE' ]
      for row in rows( database_path )
   }
   assert stored[ ( 'Indoor Orangutan Habitat Closure', '2026-05-13' ) ] == '2026-11-11'
   assert stored[ ( 'Gift shop path', '2026-06-01' ) ] == '2026-11-11'
   assert stored[ ( 'Indo-Malaya Pavilion Construction', '2026-11-11' ) ] == '2026-12-11'
   assert animals( database_path ) == [
      ( 'Fennec fox', 'Gift shop path', '2026-06-01' ),
      ( 'Sumatran orangutan', 'Indo-Malaya Pavilion Construction', '2026-11-11' ),
   ]
