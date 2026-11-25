from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.exhibit_temporary_closure_checker import ExhibitTemporaryClosureChecker
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 18 )
SCHEMA = """
CREATE TABLE Exhibit (
   NAME TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE ExhibitStatus (
   EXHIBIT TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED INTEGER NOT NULL DEFAULT 0,
   CLOSED_MESSAGE TEXT,
   CLOSED_START TEXT,
   CLOSED_END TEXT,
   CLOSED_FOR_SEASON INTEGER NOT NULL DEFAULT 0
);
"""
NAMES = [
   'Americas Pavilion',
   'Canadian Domain',
   'Eurasia Wilds',
   'Tundra Trek',
]


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def box( title: str, description: str ) -> str:
   return f'<p><strong>{ title }</strong> { description }</p>'


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Exhibit ( NAME ) VALUES ( ? )',
      [ ( name, ) for name in NAMES ],
   )
   connection.commit()
   connection.close()


def insert_status(
      path: Path,
      exhibit: str,
      message: str,
      start: str,
      end: str,
      for_season: int = 0 ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO ExhibitStatus (
               EXHIBIT,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            ) VALUES ( ?, 1, ?, ?, ?, ? )
      """,
      ( exhibit, message, start, end, for_season ),
   )
   connection.commit()
   connection.close()


def status( path: Path ) -> list[ tuple[ str, int, str | None, str | None, str | None, int ] ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      """   SELECT
               EXHIBIT,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM ExhibitStatus
            ORDER BY EXHIBIT
      """
   ).fetchall()
   connection.close()
   return [ tuple( row ) for row in rows ]


def check(
      path: Path,
      html: str,
      today: date,
      monkeypatch: pytest.MonkeyPatch ) -> int:
   monkeypatch.setattr( WebsitePage, 'fetch_text', lambda url: html )
   CheckReport.reset_fixed_count()
   return ExhibitTemporaryClosureChecker.check_schedules( path, today )


def Test_CheckSchedules_TestUndatedNotice_ExpectStandardMonthWindow(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box(
         'Weather',
         'The Canadian Domain is closed due to current weather conditions.',
      ),
   ] )

   result = check( database_path, html, TODAY, monkeypatch )

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert status( database_path ) == [
      (
         'Canadian Domain',
         1,
         'The Canadian Domain is closed due to current weather conditions.',
         '2026-11-18',
         '2026-12-18',
         0,
      ),
   ]


def Test_CheckSchedules_TestSameTodayNotice_ExpectNoSecondWrite(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box(
         'Weather',
         'The Canadian Domain is closed today due to current weather conditions.',
      ),
   ] )
   check( database_path, html, TODAY, monkeypatch )
   CheckReport.reset_fixed_count()

   result = check( database_path, html, TODAY, monkeypatch )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert status( database_path )[ 0 ][ 3 : 5 ] == ( '2026-11-18', '2026-11-18' )


def Test_CheckSchedules_TestNamedRange_ExpectThatRange(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box(
         'Maintenance',
         'The Americas Pavilion will be closed from Monday, March 23rd until Friday, March 27th due to maintenance.',
      ),
   ] )

   result = check( database_path, html, date( 2026, 3, 20 ), monkeypatch )

   assert result == 0
   assert status( database_path ) == [
      (
         'Americas Pavilion',
         1,
         'The Americas Pavilion will be closed from Monday, March 23rd until Friday, March 27th due to maintenance.',
         '2026-03-23',
         '2026-03-27',
         0,
      ),
   ]


def Test_CheckSchedules_TestMidMonthNotice_ExpectRollingEndUntilRemoved(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   message = 'The Americas Pavilion will be closed for maintenance.'
   insert_status( database_path, 'Americas Pavilion', message, '2026-11-30', '2026-11-30' )
   html = page( [ box( 'Monday, November 30 - Mid-December (Subject to Change)', message ) ] )

   assert check( database_path, html, date( 2026, 11, 25 ), monkeypatch ) == 0
   assert status( database_path )[ 0 ][ 3 : 5 ] == ( '2026-11-30', '2026-12-15' )

   assert check( database_path, html, date( 2026, 12, 3 ), monkeypatch ) == 0
   assert CheckReport.fixed_count == 0

   assert check( database_path, html, date( 2026, 12, 10 ), monkeypatch ) == 0
   assert status( database_path )[ 0 ][ 3 : 5 ] == ( '2026-11-30', '2026-12-17' )

   assert check( database_path, page( [] ), date( 2026, 12, 11 ), monkeypatch ) == 0
   assert status( database_path )[ 0 ] == (
      'Americas Pavilion', 0, None, '2026-11-30', '2026-12-10', 0,
   )


def Test_Notices_TestExpiredUndatedAndDatedNotices_ExpectAllNotices() -> None:
   message = 'The Americas Pavilion will be closed for maintenance.'
   html = page( [
      box( 'November 10-15', message ),
      box( 'Maintenance', message ),
      box( 'November 30 - mid-December', message ),
   ] )

   notices = ExhibitTemporaryClosureChecker.notices( html, NAMES, TODAY )

   assert [ notice.end for notice in notices ] == [ date( 2026, 11, 15 ), None, date( 2026, 12, 15 ) ]


def Test_CheckSchedules_TestPostedExpiredNotice_ExpectPublishedEndDate(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   message = 'The Americas Pavilion was closed for maintenance.'
   insert_status( database_path, 'Americas Pavilion', message, '2026-11-10', '2026-11-30' )
   html = page( [ box( 'November 10-15', message ) ] )

   assert check( database_path, html, TODAY, monkeypatch ) == 0
   assert CheckReport.fixed_count == 1
   assert status( database_path )[ 0 ][ 3 : 5 ] == ( '2026-11-10', '2026-11-15' )


def Test_CheckSchedules_TestNameUsedForSomethingElse_ExpectNoClosure(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      box(
         'Pathway',
         'A portion of the Eurasia Wilds loop pathway is closed due to construction.',
      ),
      box(
         'Run',
         'Tundra Trek: the path to the Caribou habitat may be closed for the entire day.',
      ),
   ] )

   result = check( database_path, html, TODAY, monkeypatch )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert status( database_path ) == []


def Test_CheckSchedules_TestMissingNotice_ExpectOpened(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status(
      database_path,
      'Canadian Domain',
      'The Canadian Domain is closed due to current weather conditions.',
      '2026-11-01',
      '2026-11-30',
   )

   result = check( database_path, page( [] ), TODAY, monkeypatch )

   assert result == 0
   assert status( database_path ) == [
      (
         'Canadian Domain',
         0,
         None,
         '2026-11-01',
         '2026-11-17',
         0,
      ),
   ]


def Test_CheckSchedules_TestSeasonalClosure_ExpectLeftAlone(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status(
      database_path,
      'Canadian Domain',
      '',
      '2026-11-01',
      '2027-03-31',
      1,
   )

   result = check( database_path, page( [] ), TODAY, monkeypatch )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert status( database_path ) == [
      ( 'Canadian Domain', 1, '', '2026-11-01', '2027-03-31', 1 ),
   ]
