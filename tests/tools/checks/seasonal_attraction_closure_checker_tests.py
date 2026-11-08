from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.seasonal_attraction_closure_checker import SeasonalAttractionClosureChecker as CHECKER
from tools.checks.website_page import WebsitePage


SPLASH = 'Splash Island'
CLIMB = 'Gorilla Climb Ropes Course'
FRONT_GATES = 'Face Painting, Caricatures and Henna! - Front Gates'
TUNDRA = 'Face Painting, Caricatures and Henna! - Tundra Trek'
KANGAROO = 'Kangaroo Walk-Thru'
FACE_PAINTING_LINK = 'https://www.torontozoo.com/tz/facepainting'
TODAY = date( 2026, 11, 2 )
UNTIL_MONTHS = {
   SPLASH: 4,
   CLIMB: 3,
   FRONT_GATES: 3,
   TUNDRA: 3,
   KANGAROO: 4,
}
SCHEMA = """
CREATE TABLE Attraction (
   NAME      TEXT NOT NULL,
   INFO_LINK TEXT NOT NULL,
   CLOSED_FOR_SEASON_UNTIL_MONTH INTEGER,
   PRIMARY KEY ( NAME )
);

CREATE TABLE AttractionStatus (
   ATTRACTION         TEXT NOT NULL,
   IS_CLOSED          BOOL NOT NULL,
   CLOSED_MESSAGE     TEXT,
   CLOSED_START       DATE,
   CLOSED_END         DATE,
   CLOSED_FOR_SEASON  BOOL NOT NULL,
   PRIMARY KEY ( ATTRACTION )
);

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);
"""




def _write_database(
      path: Path,
      attractions: list[ tuple[ str, str ] ],
      closed_for_season: list[ tuple[ str, str | None, str | None ] ],
      curves: list[ tuple[ date, float, float ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Attraction ( NAME, INFO_LINK, CLOSED_FOR_SEASON_UNTIL_MONTH ) VALUES ( ?, ?, ? )',
      [
         ( name, link, UNTIL_MONTHS.get( name ) )
         for name, link in attractions
      ],
   )

   for name, start, end in closed_for_season:
      connection.execute(
         """   INSERT INTO AttractionStatus (
                  ATTRACTION,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               ) VALUES ( ?, 1, ?, ?, 1 )
         """,
         ( name, start, end ),
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
         ( SPLASH, 'Discovery Zone', yesterday.month, yesterday.day, yesterday_value ),
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
         ( SPLASH, 'Discovery Zone', scheduled_date.month, scheduled_date.day, today_value ),
      )

   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str, str ] ] ) -> str:
   parts = []

   for href, title, status in cards:
      parts.append(
         f'<a class="col3" href="{ href }">'
         f'<div class="col3title">{ title }</div>'
         f'<span class="opentxt">{ status }</span>'
         '</a>'
      )

   return ''.join( parts )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   CheckReport.reset_fixed_count()
   result = CHECKER.check_schedules( database, today )
   return result, capsys.readouterr().out


def _season_row( database: Path, name: str ) -> tuple[ int, str | None, str | None, int ] | None:
   connection = sqlite3.connect( database )
   row = connection.execute(
      """   SELECT
               IS_CLOSED,
               CLOSED_START,
               CLOSED_END,
               CLOSED_FOR_SEASON
            FROM AttractionStatus
            WHERE ATTRACTION = ?
      """,
      ( name, ),
   ).fetchone()
   connection.close()

   if row == None:
      return None

   return ( row[ 0 ], row[ 1 ], row[ 2 ], row[ 3 ] )


def Test_CheckSchedules_TestRampDownWebsiteOnly_ExpectClosedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', 'Splash island', 'Closed For The Season' ),
         ( '/tz/kangaroo', KANGAROO, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { SPLASH }' in output
   assert 'images/details/attractions/splash-island.png' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert _season_row( database, SPLASH ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert KANGAROO not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestMayWebsiteClosed_ExpectUnchanged(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   may = date( 2027, 5, 1 )
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [],
      [ ( may, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/splash', 'Splash island', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, may, capsys )

   assert result == 0
   assert SPLASH not in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) not in output
   assert _season_row( database, SPLASH ) == None


def Test_CheckSchedules_TestAllowedWebsiteOnlyAttraction_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/kidszoo', 'Kids&nbsp;Zoo', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'Kids Zoo' not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output


def Test_CheckSchedules_TestUnmatchedWebsiteTitle_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/carousel', 'Carousel', 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert '  Carousel' in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output


def Test_CheckSchedules_TestSharedLink_ExpectBothLocationsCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( FRONT_GATES, FACE_PAINTING_LINK ),
         ( TUNDRA, FACE_PAINTING_LINK ),
      ],
      [
         ( FRONT_GATES, TODAY.isoformat(), None ),
         ( TUNDRA, TODAY.isoformat(), None ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/tz/facepainting',
            'Face Painting, Body Art, and Henna!',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert FRONT_GATES not in output
   assert TUNDRA not in output


def Test_CheckSchedules_TestSharedLinkOneLocation_ExpectClosedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( FRONT_GATES, FACE_PAINTING_LINK ),
         ( TUNDRA, FACE_PAINTING_LINK ),
      ],
      [ ( FRONT_GATES, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         (
            '/tz/facepainting',
            'Face Painting, Body Art, and Henna!',
            'Closed for the Season',
         ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { TUNDRA }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert _season_row( database, TUNDRA ) == ( 1, TODAY.isoformat(), '2027-03-31', 1 )
   assert FRONT_GATES not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output


def Test_CheckSchedules_TestRampDownAppOnly_ExpectOpenedAndClosed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   ended = TODAY - timedelta( days=1 )
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ),
         ( CLIMB, 'https://www.torontozoo.com/tz/gorillaclimb' ),
      ],
      [
         ( KANGAROO, TODAY.isoformat(), None ),
         ( CLIMB, ended.isoformat(), ended.isoformat() ),
      ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH, 'Closed For The Season' ),
         ( '/tz/kangaroo', KANGAROO, 'Open Daily' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { SPLASH }' in output
   assert f'  { KANGAROO }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, SPLASH ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert _season_row( database, KANGAROO ) == None
   assert CLIMB not in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestOpenThroughPastDate_ExpectWebsiteSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ) ],
      [ ( KANGAROO, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/kangaroo', KANGAROO, 'Open Weekends Through October 31st' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert KANGAROO not in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestOpenThroughToday_ExpectOpenedForSeason(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   through_today = date( 2026, 10, 31 )
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ) ],
      [ ( KANGAROO, through_today.isoformat(), None ) ],
      [ ( through_today, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/kangaroo', KANGAROO, 'Open Weekends Through October 31' ),
      ] ),
   )

   result, output = _check( database, through_today, capsys )

   assert result == 0
   assert f'  { KANGAROO }' in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, KANGAROO ) == None
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output


def Test_CheckSchedules_TestRampDownMatch_ExpectNoIssues(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ],
      [ ( SPLASH, TODAY.isoformat(), None ) ],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/splash', 'Splash island', 'Closed For The Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 0 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 0 ) in output


def Test_CheckSchedules_TestDifferentAttractionsClosed_ExpectBothCorrected(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( KANGAROO, 'https://www.torontozoo.com/tz/kangaroo' ),
      ],
      [ ( SPLASH, TODAY.isoformat(), None ) ],
      [ ( TODAY, 0.5, 1.0 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/kangaroo', KANGAROO, 'Closed for the Season' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert f'  { SPLASH }' in output
   assert f'  { KANGAROO }' in output
   assert CheckReport.text( 'checks.setClosedForSeasonFrom' ) in output
   assert CheckReport.text( 'checks.setOpenForSeason' ) in output
   assert _season_row( database, KANGAROO ) == ( 1, TODAY.isoformat(), '2027-04-30', 1 )
   assert _season_row( database, SPLASH ) == None
   assert CheckReport.category_line( 'checks.closedForSeasonWebsiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.closedForSeasonAppOnly', 1 ) in output


def Test_CheckSchedules_TestNoUntilMonth_ExpectCrash(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   carousel = 'Conservation Carousel'
   _write_database(
      database,
      [ ( carousel, 'https://www.torontozoo.com/tz/carousel' ) ],
      [],
      [ ( TODAY, 1.0, 0.5 ) ],
   )
   _install_page(
      monkeypatch,
      _page( [ ( '/tz/carousel', carousel, 'Closed for the Season' ) ] ),
   )

   with pytest.raises( TypeError ):
      CHECKER.check_schedules( database, TODAY )
