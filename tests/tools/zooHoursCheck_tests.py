from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

import tools.zooHoursCheck as zoo_hours_check


TODAY = date( 2026, 11, 3 )
WINTER = ( None, '09:30', '15:30', '16:30' )
CHRISTMAS = ( None, '11:00', '15:00', '16:00' )
SCHEMA = """
CREATE TABLE ZooHours (
   OPERATING_DATE DATE NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME TEXT NOT NULL,
   LAST_ADMISSION_TIME TEXT NOT NULL,
   CLOSE_TIME TEXT NOT NULL
);
"""


def _write_database(
      path: Path,
      rows: list[ tuple[ date, str | None, str, str, str ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            ) VALUES ( ?, ?, ?, ?, ? )
      """,
      [
         ( day.isoformat(), early, open_time, last_admission, close )
         for day, early, open_time, last_admission, close in rows
      ],
   )
   connection.commit()
   connection.close()


def _page(
      range_line: str,
      daily: str = 'Daily 9:30am - 4:30pm*',
      footnote: str = '*Last admission 1 hour before closing.',
      exceptions: list[ str ] | None = None ) -> str:
   extra = [] if exceptions == None else exceptions
   body = '<br />'.join( [ f'<strong>{ range_line }</strong>', daily, footnote, *extra ] )
   return f'<div id="currenthours"></div><p class="centered">{ body }</p>'


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( zoo_hours_check, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = zoo_hours_check.check_lists( database, today )
   return result, capsys.readouterr().out


def Test_ParseWebsiteHours_TestPublishedParagraph_ExpectChristmasOverride() -> None:
   page = (
      '<div id="currenthours"></div>'
      '<p class="centered"><strong style="font-weight:900;">Now Through - Friday, March 12, 2027</strong><br />'
      'Daily&nbsp;9:30am - 4:30pm*<br />'
      '*Last admission 1 hour before closing.<br />'
      '🎅Friday, December 25 11:00am - 4:00pm*</p>'
   )

   hours = zoo_hours_check.parse_website_hours( page, TODAY )

   assert hours[ TODAY ] == WINTER
   assert hours[ date( 2026, 12, 25 ) ] == CHRISTMAS
   assert hours[ date( 2027, 3, 12 ) ] == WINTER
   assert date( 2026, 11, 2 ) not in hours
   assert date( 2027, 3, 13 ) not in hours


def Test_CheckLists_TestMatchingHours_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( TODAY, *WINTER ),
         ( date( 2026, 11, 4 ), *WINTER ),
         ( date( 2026, 11, 2 ), None, '11:00', '14:00', '15:00' ),
      ],
   )
   _install_page( monkeypatch, _page( 'Now Through - Wednesday, November 4, 2026' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'On the website and not in the app: 0' in output
   assert 'In the app and not on the website: 0' in output
   assert '2026-11-02' not in output


def Test_CheckLists_TestWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( TODAY, *WINTER ) ] )
   _install_page( monkeypatch, _page( 'Now Through - Friday, November 6, 2026' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 3
   assert 'On the website and not in the app: 3' in output
   assert '  2026-11-04 to 2026-11-06 (3 days): open 09:30, last admission 15:30, close 16:30' in output
   assert 'In the app and not on the website: 0' in output


def Test_CheckLists_TestAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( TODAY, *WINTER ),
         ( date( 2026, 11, 4 ), None, '09:30', '17:00', '18:00' ),
      ],
   )
   _install_page( monkeypatch, _page( 'Now Through - Tuesday, November 3, 2026' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'In the app and not on the website: 1' in output
   assert '  2026-11-04: open 09:30, last admission 17:00, close 18:00' in output
   assert 'On the website and not in the app: 0' in output


def Test_CheckLists_TestDifferentHours_ExpectBothSides(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( TODAY, '09:00', '09:30', '15:30', '16:30' ) ] )
   _install_page( monkeypatch, _page( 'Now Through - Tuesday, November 3, 2026' ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert 'On the website and not in the app: 1' in output
   assert '  2026-11-03: open 09:30, last admission 15:30, close 16:30' in output
   assert 'In the app and not on the website: 1' in output
   assert '  2026-11-03: early admission 09:00, open 09:30, last admission 15:30, close 16:30' in output


def Test_CheckLists_TestChristmasException_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( date( 2026, 12, 24 ), *WINTER ),
         ( date( 2026, 12, 25 ), *CHRISTMAS ),
         ( date( 2026, 12, 26 ), *WINTER ),
      ],
   )
   _install_page(
      monkeypatch,
      _page(
         'Thursday, December 24, 2026 Through Saturday, December 26, 2026',
         exceptions=[ '🎅Friday, December 25 11:00am - 4:00pm*' ],
      ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert '2026-12-25' not in output


def Test_CheckLists_TestMissingHours_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [] )
   _install_page( monkeypatch, '<div id="directions">Parking</div>' )

   with pytest.raises( RuntimeError, match='The plan page has no hours list.' ):
      zoo_hours_check.check_lists( database, TODAY )


def Test_CheckLists_TestExceptionOutsideRange_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [] )
   _install_page(
      monkeypatch,
      _page(
         'Now Through - Tuesday, November 3, 2026',
         exceptions=[ 'Friday, December 25 11:00am - 4:00pm' ],
      ),
   )

   with pytest.raises( RuntimeError, match='outside the published range' ):
      zoo_hours_check.check_lists( database, TODAY )
