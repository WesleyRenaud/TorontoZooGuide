from __future__ import annotations

import sqlite3

import pytest

from api.exhibits.data_access.exhibit_provider import ExhibitProvider


EXHIBIT_PROVIDER_SCHEMA = """
CREATE TABLE Region (
   NAME TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE Exhibit (
   NAME     TEXT NOT NULL PRIMARY KEY,
   REGION   TEXT NOT NULL
);

CREATE TABLE Animal (
   SPECIES TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE Enclosure (
   SPECIES   TEXT NOT NULL,
   EXHIBIT   TEXT NOT NULL,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""

AFRICA = 'Africa'
EURASIA = 'Eurasia'
SAVANNA = 'Africa Savanna'
RAINFOREST = 'African Rainforest Pavilion'
LION = 'African Lion'
PENGUIN = 'African Penguin'
GORILLA = 'Western Lowland Gorilla'


@pytest.fixture
def exhibit_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EXHIBIT_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _seed_exhibits( conn: sqlite3.Connection ) -> None:
   conn.executemany(
      'INSERT INTO Region ( NAME ) VALUES ( ? );',
      [ ( AFRICA, ), ( EURASIA, ) ],
   )
   conn.executemany(
      'INSERT INTO Exhibit ( NAME, REGION ) VALUES ( ?, ? );',
      [
         ( SAVANNA, AFRICA ),
         ( RAINFOREST, AFRICA ),
      ],
   )
   conn.commit()


def Test_FetchExhibitNames_TestEmpty_ExpectEmptyList(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   assert ExhibitProvider.fetch_exhibit_names( exhibit_provider_conn ) == []


def Test_FetchExhibitNames_TestPopulated_ExpectNames(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )

   names = ExhibitProvider.fetch_exhibit_names( exhibit_provider_conn )

   assert set( names ) == { SAVANNA, RAINFOREST }


def Test_FetchExhibitNamesInRegion_TestMatchingRegion_ExpectRegionExhibits(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )

   names = ExhibitProvider.fetch_exhibit_names_in_region(
      exhibit_provider_conn,
      AFRICA )

   assert set( names ) == { SAVANNA, RAINFOREST }


def Test_FetchExhibitNamesInRegion_TestEmptyRegion_ExpectEmptyList(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )

   assert ExhibitProvider.fetch_exhibit_names_in_region(
      exhibit_provider_conn,
      EURASIA ) == []


def Test_FetchRegionExhibitRows_TestMixedRegions_ExpectOrderedRowsIncludingNullExhibit(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )

   rows = ExhibitProvider.fetch_region_exhibit_rows( exhibit_provider_conn )

   assert [
      ( row.region_name, row.exhibit_name )
      for row in rows
   ] == [
      ( AFRICA, SAVANNA ),
      ( AFRICA, RAINFOREST ),
      ( EURASIA, None ),
   ]


def Test_FetchAnimalNamesInExhibit_TestEmpty_ExpectEmptyList(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )

   assert ExhibitProvider.fetch_animal_names_in_exhibit(
      exhibit_provider_conn,
      SAVANNA ) == []


def Test_FetchAnimalNamesInExhibit_TestPopulated_ExpectDistinctSpecies(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   _seed_exhibits( exhibit_provider_conn )
   exhibit_provider_conn.executemany(
      'INSERT INTO Animal ( SPECIES ) VALUES ( ? );',
      [ ( LION, ), ( PENGUIN, ), ( GORILLA, ) ],
   )
   exhibit_provider_conn.executemany(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? );',
      [
         ( LION, SAVANNA ),
         ( PENGUIN, SAVANNA ),
         ( GORILLA, RAINFOREST ),
      ],
   )
   exhibit_provider_conn.commit()

   savanna_animals = ExhibitProvider.fetch_animal_names_in_exhibit(
      exhibit_provider_conn,
      SAVANNA )
   rainforest_animals = ExhibitProvider.fetch_animal_names_in_exhibit(
      exhibit_provider_conn,
      RAINFOREST )

   assert set( savanna_animals ) == { LION, PENGUIN }
   assert rainforest_animals == [ GORILLA ]
