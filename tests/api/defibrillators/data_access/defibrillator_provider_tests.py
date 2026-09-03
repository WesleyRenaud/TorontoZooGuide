from __future__ import annotations

import sqlite3

import pytest

from api.defibrillators.data_access.defibrillator_provider import DefibrillatorProvider


DEFIBRILLATOR_PROVIDER_SCHEMA = """
CREATE TABLE Defibrillator (
   X_COORD   REAL NOT NULL,
   Y_COORD   REAL NOT NULL
);
"""


@pytest.fixture
def defibrillator_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DEFIBRILLATOR_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchDefibrillators_TestEmpty_ExpectEmptyList(
      defibrillator_provider_conn: sqlite3.Connection ) -> None:
   assert DefibrillatorProvider.fetch_defibrillators(
      defibrillator_provider_conn ) == []


def Test_FetchDefibrillators_TestPopulated_ExpectMappedCoordinates(
      defibrillator_provider_conn: sqlite3.Connection ) -> None:
   defibrillator_provider_conn.execute(
      'INSERT INTO Defibrillator ( X_COORD, Y_COORD ) VALUES ( ?, ? );',
      ( 12.5, 67.5 ),
   )
   defibrillator_provider_conn.commit()

   defibrillators = DefibrillatorProvider.fetch_defibrillators(
      defibrillator_provider_conn )

   assert len( defibrillators ) == 1
   assert defibrillators[ 0 ].x_coord == 12.5
   assert defibrillators[ 0 ].y_coord == 67.5
