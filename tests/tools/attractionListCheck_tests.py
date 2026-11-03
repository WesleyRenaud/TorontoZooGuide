from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

import tools.attractionListCheck as attraction_list_check


SPLASH = 'Splash Island'
CLIMB = 'Gorilla Climb Ropes Course'
FRONT_GATES = 'Face Painting, Caricatures and Henna! - Front Gates'
TUNDRA = 'Face Painting, Caricatures and Henna! - Tundra Trek'
VR = 'Virtual Reality (VR) Theatre!'
FACE_PAINTING_LINK = 'https://www.torontozoo.com/tz/facepainting'
VR_LINK = 'https://www.torontozoo.com/tickets/wildexplorer'
TODAY = date( 2026, 11, 3 )
SCHEMA = """
CREATE TABLE Attraction (
   NAME TEXT NOT NULL,
   INFO_LINK TEXT NOT NULL,
   PRIMARY KEY ( NAME )
);
"""


def _write_database( path: Path, attractions: list[ tuple[ str, str ] ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Attraction ( NAME, INFO_LINK ) VALUES ( ?, ? )',
      attractions,
   )
   connection.commit()
   connection.close()


def _page( cards: list[ tuple[ str, str ] ] ) -> str:
   parts = [ '<a href="/tz/carousel">Conservation Carousel</a>' ]

   for href, title in cards:
      parts.append(
         f'<a class="col3" href="{ href }">'
         f'<div class="col3title">{ title }</div>'
         '</a>'
      )

   return ''.join( parts )


def _install_page( monkeypatch: pytest.MonkeyPatch, page: str ) -> None:
   def fetch_text( url: str ) -> str:
      return page

   monkeypatch.setattr( attraction_list_check, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = attraction_list_check.check_lists( database, today )
   return result, capsys.readouterr().out


def Test_CheckLists_TestWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ] )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH ),
         ( '/tz/stingray', 'Stingray Bay' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'On the website and not in the app: 1' in output
   assert '  Stingray Bay' in output
   assert 'In the app and not on the website: 0' in output
   assert 'Conservation Carousel' not in output


def Test_CheckLists_TestAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( CLIMB, 'https://www.torontozoo.com/tz/gorillaclimb' ),
      ],
   )
   _install_page( monkeypatch, _page( [ ( '/tz/splash', SPLASH ) ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert 'In the app and not on the website: 1' in output
   assert f'  { CLIMB }' in output
   assert 'On the website and not in the app: 0' in output


def Test_CheckLists_TestNormalizedNames_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( "Splash's Island", 'https://www.torontozoo.com/tz/other' ),
         ( 'TundraAir Ride (Zipline)', 'https://www.torontozoo.com/tz/tundraair' ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tickets/splash', 'Splash-Island' ),
         ( '/tickets/other', 'Splash’s Island' ),
         ( '/tickets/ride', 'TundraAir Ride' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert 'On the website and not in the app: 0' in output
   assert 'In the app and not on the website: 0' in output


def Test_CheckLists_TestSharedLink_ExpectBothAttractionsCovered(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( FRONT_GATES, FACE_PAINTING_LINK ),
         ( TUNDRA, FACE_PAINTING_LINK ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH ),
         ( '/tz/facepainting', 'Face Painting, Body Art, and Henna!' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert FRONT_GATES not in output
   assert TUNDRA not in output
   assert 'Face Painting, Body Art, and Henna!' not in output


def Test_CheckLists_TestDifferentTitleSameLink_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( VR, VR_LINK ) ] )
   _install_page(
      monkeypatch,
      _page( [ ( VR_LINK, 'Wild Explorer Virtual Reality (VR) Theatre!' ) ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert VR not in output
   assert 'Wild Explorer' not in output


def Test_CheckLists_TestDifferentLinkSameName_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( CLIMB, 'https://www.torontozoo.com/tz/gorillaclimb' ) ] )
   _install_page( monkeypatch, _page( [ ( '/tickets/gorillaclimb', CLIMB ) ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CLIMB not in output


def Test_CheckLists_TestEmptyPage_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ] )
   _install_page( monkeypatch, '<a href="/tz/splash">Splash Island</a>' )

   with pytest.raises( RuntimeError, match='The attractions page has no attraction list.' ):
      attraction_list_check.check_lists( database, TODAY )


def Test_CheckLists_TestMissingTitle_ExpectError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ] )
   _install_page(
      monkeypatch,
      '<a class="col3" href="/tz/splash"><span>Splash Island</span></a>',
   )

   with pytest.raises( RuntimeError, match='An attraction listing has no title.' ):
      attraction_list_check.check_lists( database, TODAY )


def Test_CheckLists_TestBothSides_ExpectIssueCount(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( CLIMB, 'https://www.torontozoo.com/tz/gorillaclimb' ),
      ],
   )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH ),
         ( '/tz/stingray', 'Stingray Bay' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert output.startswith( f'Attraction list check for { TODAY.isoformat() }.' )
   assert '  Stingray Bay' in output
   assert f'  { CLIMB }' in output


def Test_CheckLists_TestDuplicateCard_ExpectOneListing(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ] )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/stingray', 'Stingray Bay' ),
         ( '/tz/stingray', 'Stingray Bay' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert 'On the website and not in the app: 1' in output
   assert 'In the app and not on the website: 1' in output
   assert output.count( '  Stingray Bay' ) == 1


@pytest.mark.parametrize(
   'name',
   sorted( attraction_list_check.ALLOWED_WEBSITE_ONLY_ATTRACTIONS ),
)
def Test_CheckLists_TestAllowedWebsiteAttraction_ExpectIgnored(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch,
      name: str ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ ( SPLASH, 'https://www.torontozoo.com/tz/splash' ) ] )
   _install_page(
      monkeypatch,
      _page( [
         ( '/tz/splash', SPLASH ),
         ( '/tz/allowed', name ),
         ( '/tz/stingray', 'Stingray Bay' ),
      ] ),
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert f'  { name }' not in output
   assert '  Stingray Bay' in output
   assert 'On the website and not in the app: 1' in output


def Test_CheckLists_TestAllowedAttractionMissingFromWebsite_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         ( SPLASH, 'https://www.torontozoo.com/tz/splash' ),
         ( 'Kids Zoo', 'https://www.torontozoo.com/tz/kidszoo' ),
      ],
   )
   _install_page( monkeypatch, _page( [ ( '/tz/splash', SPLASH ) ] ) )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert '  Kids Zoo' in output
   assert 'In the app and not on the website: 1' in output
