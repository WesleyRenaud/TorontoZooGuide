from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.exhibit_season_checker import ExhibitSeasonChecker
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 11 )
MAYAN = 'Americas Outdoor Mayan Temple Ruins'
CANADIAN = 'Canadian Domain'
SCHEMA = """
CREATE TABLE Exhibit (
   NAME TEXT NOT NULL PRIMARY KEY,
   OPEN_START_MONTH INTEGER,
   OPEN_END_MONTH INTEGER
);

CREATE TABLE ExhibitStatus (
   EXHIBIT TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED INTEGER NOT NULL,
   CLOSED_MESSAGE TEXT,
   CLOSED_START TEXT,
   CLOSED_END TEXT,
   CLOSED_FOR_SEASON INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Animal (
   SPECIES TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL
);

CREATE TABLE EnclosureViewing (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   NAME TEXT
);

CREATE TABLE AnimalStatus (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   IS_OFF_DISPLAY INTEGER NOT NULL,
   VIEWING_SCOPE TEXT NOT NULL,
   OFF_DISPLAY_MESSAGE TEXT,
   OFF_DISPLAY_START TEXT,
   OFF_DISPLAY_END TEXT,
   OFF_DISPLAY_FOR_SEASON INTEGER NOT NULL,
   CLOSURE_UPDATE_TITLE TEXT,
   CLOSURE_UPDATE_START TEXT
);
"""


def _write_database(
      path: Path,
      exhibit: str,
      months: tuple[ int, int ] | None,
      species: list[ str ],
      status: tuple[ int, str, str, int ] | None = None ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   start_month = None if months is None else months[ 0 ]
   end_month = None if months is None else months[ 1 ]
   connection.execute(
      """   INSERT INTO Exhibit ( NAME, OPEN_START_MONTH, OPEN_END_MONTH )
            VALUES ( ?, ?, ? )
      """,
      ( exhibit, start_month, end_month ),
   )
   connection.executemany(
      'INSERT INTO Animal ( SPECIES ) VALUES ( ? )',
      [ ( name, ) for name in species ],
   )
   connection.executemany(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? )',
      [ ( name, exhibit ) for name in species ],
   )
   connection.executemany(
      'INSERT INTO EnclosureViewing ( SPECIES, EXHIBIT, NAME ) VALUES ( ?, ?, NULL )',
      [ ( name, exhibit ) for name in species ],
   )

   if status is not None:
      closed, start, end, for_season = status
      connection.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               ) VALUES ( ?, ?, ?, ?, ? )
         """,
         ( exhibit, closed, start, end, for_season ),
      )

   connection.commit()
   connection.close()


def _page( animals: list[ str ] ) -> str:
   cards = [
      (
         f'<a href="/animals/{ name.replace( " ", "%20" ) }">'
         '<span class="line2 status sseason">Off for the Season</span>'
         '</a>'
      )
      for name in animals
   ]
   return (
      '<div class="atitle" id="Americas">'
      + ''.join( cards )
      + '</div>'
   )


def _install_page( monkeypatch: pytest.MonkeyPatch, animals: list[ str ] ) -> None:
   def fetch_text( url: str ) -> str:
      return _page( animals )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   CheckReport.reset_fixed_count()
   result = ExhibitSeasonChecker.check_schedules( database, TODAY )
   return result, capsys.readouterr().out


def _status( database: Path ) -> tuple[ int, str, str, int ]:
   connection = sqlite3.connect( database )
   row = connection.execute(
      """   SELECT IS_CLOSED, CLOSED_START, CLOSED_END, CLOSED_FOR_SEASON
            FROM ExhibitStatus
      """
   ).fetchone()
   connection.close()
   return ( row[ 0 ], row[ 1 ], row[ 2 ], row[ 3 ] )


def _animal_ends( database: Path ) -> list[ tuple[ str, str, str, int ] ]:
   connection = sqlite3.connect( database )
   rows = connection.execute(
      """   SELECT SPECIES, OFF_DISPLAY_START, OFF_DISPLAY_END, OFF_DISPLAY_FOR_SEASON
            FROM AnimalStatus
            ORDER BY SPECIES
      """
   ).fetchall()
   connection.close()
   return [ ( row[ 0 ], row[ 1 ], row[ 2 ], row[ 3 ] ) for row in rows ]


def Test_CheckSchedules_TestEveryAnimalOff_ExpectExhibitClosed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   species = [ 'Capybara', 'Turkey Vulture' ]
   _write_database( database, MAYAN, ( 4, 10 ), species )
   _install_page( monkeypatch, [ 'Turkey vulture', 'Capybara' ] )

   result, output = _check( database, capsys )

   assert result == 0
   assert MAYAN in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert 'March 31, 2027' in output
   assert _status( database ) == ( 1, '2026-11-11', '2027-03-31', 1 )
   assert _animal_ends( database ) == [
      ( 'Capybara', '2026-11-11', '2027-03-31', 1 ),
      ( 'Turkey Vulture', '2026-11-11', '2027-03-31', 1 ),
   ]


def Test_CheckSchedules_TestAppClosedWebOpen_ExpectReopened(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      CANADIAN,
      ( 4, 11 ),
      [ 'Moose', 'Bison' ],
      ( 1, '2026-11-01', '2027-03-31', 1 ),
   )
   _install_page( monkeypatch, [ 'Moose' ] )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.text( 'checks.setOpenForSeasonFrom' ) in output
   assert 'November 30, 2026' in output
   assert _status( database ) == ( 0, '2026-11-11', '2026-11-30', 0 )
   assert _animal_ends( database ) == []


def Test_CheckSchedules_TestClosedBeyondTheWindow_ExpectShortened(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      MAYAN,
      ( 4, 10 ),
      [ 'Turkey Vulture' ],
      ( 1, '2026-10-01', '2027-06-30', 1 ),
   )
   _install_page( monkeypatch, [ 'Turkey vulture' ] )

   result, output = _check( database, capsys )

   assert result == 0
   assert _status( database ) == ( 1, '2026-10-01', '2027-03-31', 1 )
   assert _animal_ends( database ) == [
      ( 'Turkey Vulture', '2026-10-01', '2027-03-31', 1 ),
   ]


def Test_CheckSchedules_TestOpenBeyondTheWindow_ExpectShortened(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      CANADIAN,
      ( 4, 11 ),
      [ 'Moose', 'Bison' ],
      ( 0, '2026-04-01', '2026-12-31', 0 ),
   )
   _install_page( monkeypatch, [ 'Moose' ] )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.text( 'checks.setOpenForSeasonFrom' ) in output
   assert _status( database ) == ( 0, '2026-04-01', '2026-11-30', 0 )


def Test_CheckSchedules_TestMaintenanceClosure_ExpectLeftAlone(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      CANADIAN,
      ( 4, 11 ),
      [ 'Moose' ],
      ( 1, '2026-11-01', '2026-11-20', 0 ),
   )
   _install_page( monkeypatch, [] )

   result, output = _check( database, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 0 ) in output
   assert _status( database ) == ( 1, '2026-11-01', '2026-11-20', 0 )
