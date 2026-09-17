from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_enclosure_exhibit_name_provider import AnimalEnclosureExhibitNameProvider


LION = 'African Lion'
CAMEL = 'Bactrian Camel'
SAVANNA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'
CANADIAN_DOMAIN = 'Canadian Domain'

ENCLOSURE_SCHEMA = """
CREATE TABLE Enclosure (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""


@pytest.fixture
def enclosure_exhibit_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ENCLOSURE_SCHEMA )

   yield conn

   conn.close()


def _insert_enclosure(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str ) -> None:
   conn.execute(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT
            )
            VALUES ( ?, ? );
      """,
      ( species, exhibit ) )
   conn.commit()


def Test_FetchExhibitNamesForSpecies_TestEmpty_ExpectEmptyList(
      enclosure_exhibit_conn: sqlite3.Connection ) -> None:
   assert AnimalEnclosureExhibitNameProvider.fetch_exhibit_names_for_species(
      enclosure_exhibit_conn,
      LION ) == []


def Test_FetchExhibitNamesForSpecies_TestMultipleExhibits_ExpectSortedExhibits(
      enclosure_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_enclosure(
      enclosure_exhibit_conn,
      species=CAMEL,
      exhibit=EURASIA )
   _insert_enclosure(
      enclosure_exhibit_conn,
      species=CAMEL,
      exhibit=CANADIAN_DOMAIN )
   _insert_enclosure(
      enclosure_exhibit_conn,
      species=LION,
      exhibit=SAVANNA )

   assert AnimalEnclosureExhibitNameProvider.fetch_exhibit_names_for_species(
      enclosure_exhibit_conn,
      CAMEL ) == [ CANADIAN_DOMAIN, EURASIA ]


def Test_FetchExhibitNamesForSpecies_TestUniqueSpecies_ExpectSingleExhibit(
      enclosure_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_enclosure(
      enclosure_exhibit_conn,
      species=LION,
      exhibit=SAVANNA )

   assert AnimalEnclosureExhibitNameProvider.fetch_exhibit_names_for_species(
      enclosure_exhibit_conn,
      LION ) == [ SAVANNA ]
