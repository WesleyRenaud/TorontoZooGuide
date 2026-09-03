from __future__ import annotations

import sqlite3

import pytest

from api.pavilions.data_access.pavilion_provider import PavilionProvider

PAVILION_PROVIDER_SCHEMA = """
CREATE TABLE Pavilion (
   NAME          TEXT NOT NULL PRIMARY KEY,
   REGION        TEXT,
   DESCRIPTION   TEXT NOT NULL,
   X_COORD       REAL NOT NULL,
   Y_COORD       REAL NOT NULL
);
"""

AFRICAN_RAINFOREST = 'African Rainforest Pavilion'
AMERICAS = 'Americas Pavilion'

@pytest.fixture
def pavilion_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( PAVILION_PROVIDER_SCHEMA )

   yield conn

   conn.close()

def _insert_pavilion(
      conn: sqlite3.Connection,
      *,
      name: str,
      region: str = 'Africa' ) -> None:
   conn.execute(
      """   INSERT INTO Pavilion (
               NAME,
               REGION,
               DESCRIPTION,
               X_COORD,
               Y_COORD
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( name, region, f'{ name } description', 1.0, 2.0 ),
   )

def Test_FetchPavilions_TestEmpty_ExpectEmptyList(
      pavilion_provider_conn: sqlite3.Connection ) -> None:
   assert PavilionProvider.fetch_pavilions( pavilion_provider_conn ) == []

def Test_FetchPavilions_TestPopulated_ExpectMappedFields(
      pavilion_provider_conn: sqlite3.Connection ) -> None:
   _insert_pavilion( pavilion_provider_conn, name=AFRICAN_RAINFOREST )
   _insert_pavilion(
      pavilion_provider_conn,
      name=AMERICAS,
      region='Americas' )
   pavilion_provider_conn.commit()

   pavilions = PavilionProvider.fetch_pavilions( pavilion_provider_conn )

   assert { pavilion.name for pavilion in pavilions } == {
      AFRICAN_RAINFOREST,
      AMERICAS,
   }
   rainforest = next(
      pavilion
      for pavilion in pavilions
      if pavilion.name == AFRICAN_RAINFOREST )
   assert rainforest.region == 'Africa'
   assert rainforest.description == f'{ AFRICAN_RAINFOREST } description'
   assert rainforest.x_coord == 1.0
   assert rainforest.y_coord == 2.0
