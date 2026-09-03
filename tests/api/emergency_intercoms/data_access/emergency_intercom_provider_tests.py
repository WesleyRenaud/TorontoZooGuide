from __future__ import annotations

import sqlite3

import pytest

from api.emergency_intercoms.data_access.emergency_intercom_provider import EmergencyIntercomProvider


EMERGENCY_INTERCOM_PROVIDER_SCHEMA = """
CREATE TABLE EmergencyIntercom (
   X_COORD   REAL NOT NULL,
   Y_COORD   REAL NOT NULL
);
"""


@pytest.fixture
def emergency_intercom_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EMERGENCY_INTERCOM_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchEmergencyIntercoms_TestEmpty_ExpectEmptyList(
      emergency_intercom_provider_conn: sqlite3.Connection ) -> None:
   assert EmergencyIntercomProvider.fetch_emergency_intercoms(
      emergency_intercom_provider_conn ) == []


def Test_FetchEmergencyIntercoms_TestPopulated_ExpectMappedCoordinates(
      emergency_intercom_provider_conn: sqlite3.Connection ) -> None:
   emergency_intercom_provider_conn.execute(
      'INSERT INTO EmergencyIntercom ( X_COORD, Y_COORD ) VALUES ( ?, ? );',
      ( 1.0, 2.0 ),
   )
   emergency_intercom_provider_conn.commit()

   intercoms = EmergencyIntercomProvider.fetch_emergency_intercoms(
      emergency_intercom_provider_conn )

   assert len( intercoms ) == 1
   assert intercoms[ 0 ].x_coord == 1.0
   assert intercoms[ 0 ].y_coord == 2.0
