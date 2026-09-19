from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_viewing_scope_provider import AnimalViewingScopeProvider
from api.animals.domain.animal_viewing_scope import AnimalViewingScope


ENCLOSURE_VIEWING_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES          TEXT NOT NULL,
   EXHIBIT          TEXT NOT NULL,
   NAME             TEXT,
   ENCLOSURE_TYPE   TEXT NOT NULL
);
"""


@pytest.fixture
def viewing_scope_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ENCLOSURE_VIEWING_SCHEMA )

   yield conn

   conn.close()


def Test_FetchAnimalViewingScopes_TestNoRows_ExpectEmptyList(
      viewing_scope_conn: sqlite3.Connection ) -> None:
   assert AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
      viewing_scope_conn,
      species='African Lion',
      exhibit='Africa Savanna',
   ) == []


def Test_FetchAnimalViewingScopes_TestNamedAndUnnamed_ExpectSortedNames(
      viewing_scope_conn: sqlite3.Connection ) -> None:
   viewing_scope_conn.executemany(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME,
               ENCLOSURE_TYPE
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( 'Wood Bison', 'Canadian Domain', 'Female Herd', 'Outdoor' ),
         ( 'Wood Bison', 'Canadian Domain', 'Male Herd', 'Outdoor' ),
         ( 'African Lion', 'Africa Savanna', None, 'Outdoor' ),
      ],
   )
   viewing_scope_conn.commit()

   assert AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
      viewing_scope_conn,
      species='Wood Bison',
      exhibit='Canadian Domain',
   ) == [
      AnimalViewingScope.from_enclosure_name( 'Female Herd' ),
      AnimalViewingScope.from_enclosure_name( 'Male Herd' ),
   ]
   assert AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
      viewing_scope_conn,
      species='African Lion',
      exhibit='Africa Savanna',
   ) == [
      AnimalViewingScope.from_enclosure_name( None ),
   ]
