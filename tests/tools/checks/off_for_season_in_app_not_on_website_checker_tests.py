from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.off_for_season_in_app_not_on_website_checker import OffForSeasonInAppNotOnWebsiteChecker as CHECKER
from tools.checks.website_page import WebsitePage


STORK = 'Marabou Stork'
TORTOISE = 'African Spurred Tortoise'
TODAY = date( 2026, 11, 2 )
STEADY = date( 2026, 7, 15 )
SCHEMA = """
CREATE TABLE Animal (
   SPECIES TEXT NOT NULL,
   PRIMARY KEY ( SPECIES )
);

CREATE TABLE AnimalStatus (
   SPECIES                 TEXT NOT NULL,
   EXHIBIT                 TEXT NOT NULL,
   IS_OFF_DISPLAY          BOOL NOT NULL,
   VIEWING_SCOPE           TEXT NOT NULL,
   OFF_DISPLAY_MESSAGE     TEXT,
   OFF_DISPLAY_START       DATE,
   OFF_DISPLAY_END         DATE,
   OFF_DISPLAY_FOR_SEASON  BOOL NOT NULL
);

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);

CREATE TABLE Exhibit (
   NAME TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);

CREATE TABLE ExhibitStatus (
   EXHIBIT            TEXT NOT NULL,
   IS_CLOSED          BOOL NOT NULL,
   CLOSED_MESSAGE     TEXT,
   CLOSED_START       DATE,
   CLOSED_END         DATE,
   CLOSED_FOR_SEASON  BOOL NOT NULL
);

CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH INTEGER
);

CREATE TABLE EnclosureViewing (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   NAME TEXT
);
"""




def _write_database(
      path: Path,
      species: list[ str ],
      off_season: list[ tuple[ str, str, str | None ] ],
      curves: list[ tuple[ date, float, float ] ],
      closures: list[ tuple[ str, str | None, str | None, bool ] ] | None = None,
      home_exhibit: str = 'Africa Savanna',
      until_month: int = 4 ) -> None:
   if closures == None:
      closures = []

   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Animal ( SPECIES ) VALUES ( ? )',
      [ ( name, ) for name in species ],
   )
   connection.executemany(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT,
               OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
            )
            VALUES ( ?, ?, ? )
      """,
      [ ( name, home_exhibit, until_month ) for name in species ],
   )
   connection.executemany(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME
            )
            VALUES ( ?, ?, ? )
      """,
      [ ( name, home_exhibit, None ) for name in species ],
   )

   for name, start, end in off_season:
      connection.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  VIEWING_SCOPE,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_FOR_SEASON
               ) VALUES ( ?, ?, 1, ?, ?, ?, 1 )
         """,
         ( name, 'Africa Savanna', name, start, end ),
      )

   for scheduled_date, yesterday_value, today_value in curves:
      yesterday = scheduled_date - timedelta( days=1 )
      connection.execute(
         """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
                  SPECIES,
                  EXHIBIT,
                  MONTH,
                  DAY,
                  VALUE
               ) VALUES ( ?, ?, ?, ?, ? )
         """,
         ( STORK, 'Africa Savanna', yesterday.month, yesterday.day, yesterday_value ),
      )
      connection.execute(
         """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
                  SPECIES,
                  EXHIBIT,
                  MONTH,
                  DAY,
                  VALUE
               ) VALUES ( ?, ?, ?, ?, ? )
         """,
         ( STORK, 'Africa Savanna', scheduled_date.month, scheduled_date.day, today_value ),
      )

   for exhibit, start, end, closed_for_season in closures:
      connection.execute(
         'INSERT INTO Exhibit ( NAME ) VALUES ( ? )',
         ( exhibit, ),
      )
      connection.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               ) VALUES ( ?, 1, ?, ?, ? )
         """,
         ( exhibit, start, end, 1 if closed_for_season else 0 ),
      )

   connection.commit()
   connection.close()


def _page( animals: list[ str ], section: str = 'Africa Savanna' ) -> str:
   cards = []

   for name in animals:
      href = name.replace( ' ', '%20' )
      cards.append(
         f'<a href="/animals/{ href }">'
         '<span class="line2 status sseason">Off for the Season</span>'
         '</a>'
      )

   cards.append(
      '<a href="/animals/Brush-tailed%20bettong">'
      '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
      '</a>'
   )
   return (
      '<h2>Animals Not Currently Viewable</h2>'
      f'<div class="atitle scrolling-title" id="{ section }">'
      + ''.join( cards )
      + '</div>'
   )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = CHECKER.check_schedules( database, today )
   return result, capsys.readouterr().out


def Test_CheckSchedules_TestRampDownAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   today = STEADY
   database = tmp_path / 'animals.db'
   ended = today - timedelta( days=1 )
   _write_database(
      database,
      [ STORK, TORTOISE ],
      [
         ( STORK, today.isoformat(), None ),
         ( TORTOISE, None, ended.isoformat() ),
      ],
      [ ( today, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [] ) )

   result, output = _check( database, today, capsys )

   connection = sqlite3.connect( database )
   species = connection.execute( 'SELECT SPECIES FROM AnimalStatus' ).fetchall()
   connection.close()

   assert result == 0
   assert f'  { STORK }' in output
   assert AnimalDetailImage.source( 'Africa Savanna', STORK ) in output
   assert CheckReport.text( 'checks.setOnDisplayForSeason' ) in output
   assert TORTOISE not in output
   assert species == [ ( TORTOISE, ) ]
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.offForSeasonWebsiteOnly', 0 ) not in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK ],
      [ ( STORK, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 0.5 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Marabou stork' ] ) )

   result, output = _check( database, STEADY, capsys )

   connection = sqlite3.connect( database )
   species = connection.execute( 'SELECT SPECIES FROM AnimalStatus' ).fetchall()
   connection.close()

   assert result == 0
   assert species == [ ( STORK, ) ]
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.offForSeasonWebsiteOnly', 0 ) not in output


def Test_CheckSchedules_TestDifferentAnimalsOffDisplay_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK, TORTOISE ],
      [ ( STORK, STEADY.isoformat(), None ) ],
      [],
   )
   _install_page( monkeypatch, _page( [ TORTOISE ] ) )

   result, output = _check( database, STEADY, capsys )

   connection = sqlite3.connect( database )
   species = connection.execute( 'SELECT SPECIES FROM AnimalStatus' ).fetchall()
   connection.close()

   assert result == 0
   assert f'  { STORK }' in output
   assert species == []
   assert TORTOISE not in output
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestMarchStorkOffInApp_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   today = date( 2026, 3, 15 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ 'Zebra', STORK ],
      [ ( STORK, today.isoformat(), None ) ],
      [],
   )
   _install_page( monkeypatch, _page( [ 'Zebra' ] ) )

   result, output = _check( database, today, capsys )

   connection = sqlite3.connect( database )
   species = connection.execute( 'SELECT SPECIES FROM AnimalStatus' ).fetchall()
   connection.close()

   assert result == 0
   assert f'  { STORK }' in output
   assert species == []
   assert 'Zebra' not in output
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestFebruary_ExpectCompared(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ 'Zebra' ], [], [] )
   _install_page( monkeypatch, _page( [ 'Zebra' ] ) )

   result, output = _check( database, date( 2026, 2, 1 ), capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 0 ) in output
   assert 'Zebra' not in output


def Test_CheckSchedules_TestOffDisplayOnSteadyDate_ExpectNoAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK ],
      [ ( STORK, STEADY.isoformat(), None ) ],
      [ ( STEADY, 1.0, 1.0 ) ],
   )
   _install_page( monkeypatch, _page( [ 'Marabou stork' ] ) )

   result, output = _check( database, STEADY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.offForSeasonAppOnly', 0 ) in output
   assert f'  { STORK }' not in output


def Test_CheckSchedules_TestNovember_ExpectNotCompared(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ STORK ],
      [ ( STORK, TODAY.isoformat(), None ) ],
      [],
   )

   def fetch_text( url: str ) -> str:
      raise AssertionError( 'fetch_text' )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )

   result, output = _check( database, TODAY, capsys )

   connection = sqlite3.connect( database )
   species = connection.execute( 'SELECT SPECIES FROM AnimalStatus' ).fetchall()
   connection.close()

   assert result == 0
   assert output == ''
   assert species == [ ( STORK, ) ]
