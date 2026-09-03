from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_viewing_scope_provider import AnimalViewingScopeProvider
from api.shared.enums import AnimalViewingScope


ENCLOSURE_VIEWING_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES          TEXT NOT NULL,
   EXHIBIT          TEXT NOT NULL,
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


def Test_FetchAnimalViewingScopes_TestDistinctScopes_ExpectNormalizedScopes(
      viewing_scope_conn: sqlite3.Connection ) -> None:
   viewing_scope_conn.executemany(
      'INSERT INTO EnclosureViewing ( SPECIES, EXHIBIT, ENCLOSURE_TYPE ) VALUES ( ?, ?, ? );',
      [
         ( 'African Lion', 'Africa Savanna', 'Indoor' ),
         ( 'African Lion', 'Africa Savanna', 'indoor' ),
         ( 'African Lion', 'Africa Savanna', 'Outdoor' ),
         ( 'African Lion', 'Africa Savanna', 'aviary' ),
      ],
   )
   viewing_scope_conn.commit()

   assert AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
      viewing_scope_conn,
      species='African Lion',
      exhibit='Africa Savanna',
   ) == [
      AnimalViewingScope.INDOOR,
      AnimalViewingScope.OUTDOOR,
   ]
