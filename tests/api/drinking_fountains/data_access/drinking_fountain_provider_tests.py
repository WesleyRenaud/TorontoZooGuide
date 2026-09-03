from __future__ import annotations

import sqlite3

import pytest

from api.drinking_fountains.data_access.drinking_fountain_provider import DrinkingFountainProvider


DRINKING_FOUNTAIN_PROVIDER_SCHEMA = """
CREATE TABLE DrinkingFountain (
   X_COORD   REAL NOT NULL,
   Y_COORD   REAL NOT NULL
);
"""


@pytest.fixture
def drinking_fountain_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DRINKING_FOUNTAIN_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchDrinkingFountainRecords_TestEmpty_ExpectEmptyList(
      drinking_fountain_provider_conn: sqlite3.Connection ) -> None:
   assert DrinkingFountainProvider.fetch_drinking_fountain_records(
      drinking_fountain_provider_conn ) == []


def Test_FetchDrinkingFountainRecords_TestPopulated_ExpectMappedCoordinates(
      drinking_fountain_provider_conn: sqlite3.Connection ) -> None:
   drinking_fountain_provider_conn.execute(
      'INSERT INTO DrinkingFountain ( X_COORD, Y_COORD ) VALUES ( ?, ? );',
      ( 4.5, 8.25 ),
   )
   drinking_fountain_provider_conn.commit()

   fountains = DrinkingFountainProvider.fetch_drinking_fountain_records(
      drinking_fountain_provider_conn )

   assert len( fountains ) == 1
   assert fountains[ 0 ].x_coord == 4.5
   assert fountains[ 0 ].y_coord == 8.25
