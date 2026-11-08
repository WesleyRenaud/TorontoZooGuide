from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3
from urllib.parse import quote

import pytest

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.app_string_provider import AppStringProvider
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.animal_list_checker import AnimalListChecker as animal_list_checker
from tools.checks.check_report import CheckReport
from tools.checks.website_page import WebsitePage


LION = 'African Lion'
LAU = 'Lau Banded Iguana'
TODAY = date( 2026, 11, 3 )
SCHEMA = """
CREATE TABLE Animal (
   SPECIES TEXT NOT NULL,
   PRIMARY KEY ( SPECIES )
);
CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL
);
"""


def _write_database( path: Path, species: list[ str ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Animal ( SPECIES ) VALUES ( ? )',
      [ ( name, ) for name in species ],
   )
   connection.executemany(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? )',
      [ ( name, 'Africa Savanna' ) for name in species ],
   )
   connection.commit()
   connection.close()


def _page( names: list[ str ], exhibit: str = 'Africa Savanna' ) -> str:
   parts = [ f'<h1>{ exhibit }</h1><a href="/animals/africa">Africa</a>' ]

   for name in names:
      href = quote( name, safe='' )
      parts.append( f'<a href="/animals/{ href }" class="thm"></a>' )

   return ''.join( parts )


def _install_pages(
      monkeypatch: pytest.MonkeyPatch,
      extras: dict[ str, list[ str ] ] | None = None,
      shared: list[ str ] | None = None ) -> None:
   extra_names = {} if extras == None else extras
   shared_names = [ LION ] if shared == None else shared

   def fetch_text( url: str ) -> str:
      path = url.rstrip( '/' ).rsplit( '/', 1 )[ -1 ]
      page = _page( shared_names )
      exhibit = 'Australasia Pavilion' if path == 'australasia' else 'Africa Savanna'
      return page + _page( extra_names.get( path, [] ), exhibit )

   monkeypatch.setattr( WebsitePage, 'fetch_text', fetch_text )


def _check(
      database: Path,
      today: date,
      capsys: pytest.CaptureFixture[ str ] ) -> tuple[ int, str ]:
   result = animal_list_checker.check_lists( database, today )
   return result, capsys.readouterr().out


def Test_CheckLists_TestWebsiteOnly_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ LION ] )
   _install_pages( monkeypatch, { 'africa': [ 'Tiger' ] } )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 1 ) in output
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first='Tiger', second='Africa Savanna' ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


def Test_CheckLists_TestAppOnly_ExpectAppMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ LION, 'Penguin' ] )
   _install_pages( monkeypatch )

   result, output = _check( database, TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
   assert '  Penguin' in output
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 0 ) in output


def Test_CheckLists_TestNormalizedNames_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         LION,
         'Naked Mole Rat',
         "Hamilton's Pond Turtle",
         'Green-Winged Dove',
         'Mantella (Poison Frog)',
      ],
   )
   _install_pages(
      monkeypatch,
      {
         'africa': [
            'naked mole-rat',
            'Hamilton’s Pond Turtle',
            'Green-winged dove (grey-capped emerald dove)',
            'Mantella (Poison Frog)',
         ],
      },
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 0 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


def Test_CheckLists_TestKnownWebsiteAliases_ExpectMatched(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database(
      database,
      [
         LION,
         "Edwards's Pheasant",
         'Live Reef Corals',
         'White Rhinoceros',
         'Tri-Colour Shark',
         'Wood Bison',
      ],
   )
   _install_pages(
      monkeypatch,
      {
         'africa': [
            'Edwards’s pheasant',
            'Live reef corals',
            'White rhinoceros',
            'Tri-colour shark',
            'Wood bison - female herd',
            'Wood bison - male herd',
         ],
      },
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert "Edwards's Pheasant" not in output
   assert 'White Rhinoceros' not in output
   assert 'Wood bison' not in output


def Test_CheckLists_TestDifferentSpellingsOnTwoExhibits_ExpectTwoListings(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ LION ] )
   _install_pages(
      monkeypatch,
      {
         'africa': [ 'Lau Banded Iguana' ],
         'australasia': [ 'Lau banded iguana' ],
      },
   )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 2 ) in output
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first=LAU, second='Africa Savanna' ) in output
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first='Lau banded iguana', second='Australasia Pavilion' ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


def Test_CheckLists_TestBothSides_ExpectIssueCount(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ LION, 'Penguin' ] )
   _install_pages( monkeypatch, { 'tundra': [ 'Tiger' ] } )

   result, output = _check( database, TODAY, capsys )

   assert result == 2
   assert output.startswith( f'Animal list check for { TODAY.isoformat() }.' )
   assert '  Tiger' in output
   assert '  Penguin' in output


def Test_CheckLists_TestZebraInCanada_ExpectAllowed(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ LION, "Grevy's Zebra" ] )
   connection = sqlite3.connect( database )
   connection.execute(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? )',
      ( "Grevy's Zebra", 'Canadian Domain' ),
   )
   connection.commit()
   connection.close()
   _install_pages( monkeypatch, { 'africa': [ "Grevy's Zebra" ] } )

   result, output = _check( database, TODAY, capsys )

   assert result == 0
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first="Grevy's Zebra", second='Canadian Domain' ) not in output
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 0 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 0 ) in output


@pytest.mark.parametrize(
   ( 'species', 'exhibit' ),
   sorted( animal_list_checker.ALLOWED_APP_ONLY_ANIMALS ),
)
def Test_CheckLists_TestAllowedPairAndOtherExhibit_ExpectOnlyOtherExhibitFlagged(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch,
      species: str,
      exhibit: str ) -> None:
   monkeypatch.setattr(
      animal_list_checker,
      'load_species',
      lambda database: [
         AnimalSpeciesExhibit( species=species, exhibit=exhibit ),
         AnimalSpeciesExhibit( species=species, exhibit='Other Exhibit' ),
      ],
   )
   monkeypatch.setattr( animal_list_checker, 'fetch_website_animals', lambda: [] )

   result, output = _check( tmp_path / 'animals.db', TODAY, capsys )

   assert result == 1
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first=species, second='Other Exhibit' ) in output
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first=species, second=exhibit ) not in output


def Test_CheckLists_TestAllowedPairMissingFromApp_ExpectWebsiteMiss(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( animal_list_checker, 'load_species', lambda database: [] )
   monkeypatch.setattr(
      animal_list_checker,
      'fetch_website_animals',
      lambda: [
         AnimalSpeciesExhibit( species="Grevy's Zebra", exhibit='Canadian Domain' ),
      ],
   )

   result, output = _check( tmp_path / 'animals.db', TODAY, capsys )

   assert result == 1
   assert CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 1 ) in output
   assert '  ' + AppStringProvider.format( 'format.middleDotPair', first="Grevy's Zebra", second='Canadian Domain' ) in output


def Test_CheckLists_TestWebsiteMissAtKnownExhibit_ExpectAppPhoto(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( animal_list_checker, 'load_species', lambda database: [] )
   monkeypatch.setattr(
      animal_list_checker,
      'fetch_website_animals',
      lambda: [
         AnimalSpeciesExhibit( species='Red Panda', exhibit='Africa Savanna' ),
      ],
   )

   result, output = _check( tmp_path / 'animals.db', TODAY, capsys )
   photo = AnimalDetailImage.source( 'Africa Savanna', 'Red Panda' )

   assert result == 1
   assert photo in output
   assert 'Eurasia Wilds' not in output


def Test_ParseWebsiteAnimals_TestHeadingWithBreak_ExpectExhibitName() -> None:
   page = _page( [ LION ], 'Americas Outdoor<br />Mayan Temple Ruins' )

   listings = animal_list_checker.parse_website_animals( page )

   assert listings == [
      AnimalSpeciesExhibit(
         species=LION,
         exhibit='Americas Outdoor Mayan Temple Ruins',
      ),
   ]
