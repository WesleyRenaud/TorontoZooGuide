from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.station_closure_checker import StationClosureChecker
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 14 )
EURASIA = 'Eurasia Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
MESSAGE = 'The Eurasia Zoomobile stop is closed at this time.'
SRT = (
   'The Scarborough Rapid Transit (SRT) car at the Tundra Zoomobile Station '
   'will be closed for a private event.'
)
SCHEMA = """
CREATE TABLE TransportationStationStatus (
   TRANSPORTATION TEXT NOT NULL,
   STATION TEXT NOT NULL,
   IS_CLOSED INTEGER NOT NULL DEFAULT 0,
   CLOSED_MESSAGE TEXT,
   CLOSED_START TEXT,
   CLOSED_END TEXT,
   PRIMARY KEY (TRANSPORTATION, STATION)
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


def insert_status(
      path: Path,
      station: str,
      is_closed: int,
      message: str,
      start: str,
      end: str | None ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO TransportationStationStatus (
               TRANSPORTATION, STATION, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            ) VALUES ( 'Zoomobile', ?, ?, ?, ?, ? )
      """,
      ( station, is_closed, message, start, end ),
   )
   connection.commit()
   connection.close()


def status_rows( path: Path ) -> dict[ str, tuple[ int, str | None, str | None, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = {
      row[ 0 ]: ( row[ 1 ], row[ 2 ], row[ 3 ], row[ 4 ] )
      for row in connection.execute(
         """   SELECT STATION, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
               FROM TransportationStationStatus
         """
      )
   }
   connection.close()
   return loaded


def Test_CheckSchedules_TestUndatedNotice_ExpectTwoWeekClosure(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         (
            '<p><strong>Eurasia pathway</strong> '
            'The Eurasia Zoomobile stop is closed at this time.</p>'
         ),
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = StationClosureChecker.check_schedules( database_path, TODAY )
   output = capsys.readouterr().out

   assert result == 0
   assert status_rows( database_path )[ EURASIA ] == (
      1,
      MESSAGE,
      '2026-11-14',
      '2026-11-28',
   )
   assert MESSAGE in output
   assert 'Set the station from November 14, 2026 through November 28, 2026.' in output


def Test_CheckSchedules_TestStaleClosure_ExpectDeleted(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status( database_path, EURASIA, 1, MESSAGE, '2026-11-01', '2026-12-01' )
   insert_status(
      database_path,
      TUNDRA,
      1,
      'The Tundra Zoomobile Station is temporarily closed.',
      '2026-04-23',
      '2026-04-30',
   )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         '<p><strong>Eurasia</strong> The Eurasia Zoomobile stop is now open.</p>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = StationClosureChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert EURASIA not in status_rows( database_path )
   assert status_rows( database_path )[ TUNDRA ][ 2 : ] == ( '2026-04-23', '2026-04-30' )


def Test_CheckSchedules_TestSoonerEnd_ExpectExtended(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status( database_path, EURASIA, 1, MESSAGE, '2026-11-01', '2026-11-20' )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         (
            '<p><strong>Eurasia pathway</strong> '
            'The Eurasia Zoomobile stop is closed at this time.</p>'
         ),
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = StationClosureChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert status_rows( database_path )[ EURASIA ][ 2 : ] == ( '2026-11-01', '2026-11-28' )


def Test_CheckSchedules_TestPageRange_ExpectStoredRange(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status( database_path, TUNDRA, 1, SRT, '2026-04-20', '2026-04-30' )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         (
            '<p><strong>Monday, April 20 - Wednesday, April 22</strong> '
            'The Scarborough Rapid Transit (SRT) car at the Tundra Zoomobile Station '
            'will be closed for a private event.</p>'
         ),
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = StationClosureChecker.check_schedules( database_path, date( 2026, 4, 21 ) )

   assert result == 0
   assert status_rows( database_path )[ TUNDRA ][ 2 : ] == ( '2026-04-20', '2026-04-22' )


def Test_CheckSchedules_TestChangedMessage_ExpectReplaced(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   replacement = 'The Eurasia Zoomobile station is closed for maintenance.'
   insert_status( database_path, EURASIA, 1, MESSAGE, '2026-11-01', '2026-12-01' )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         f'<p><strong>Eurasia</strong> { replacement }</p>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = StationClosureChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert status_rows( database_path )[ EURASIA ] == (
      1,
      replacement,
      '2026-11-14',
      '2026-11-28',
   )
