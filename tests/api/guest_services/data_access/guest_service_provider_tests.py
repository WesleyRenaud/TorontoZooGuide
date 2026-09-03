from __future__ import annotations

import sqlite3

import pytest

from api.guest_services.data_access.guest_service_provider import GuestServiceProvider


GUEST_SERVICE_PROVIDER_SCHEMA = """
CREATE TABLE GuestService (
   SERVICE_TYPE   TEXT NOT NULL,
   X_COORD        REAL NOT NULL,
   Y_COORD        REAL NOT NULL
);
"""

FIRST_AID = 'First Aid'


@pytest.fixture
def guest_service_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( GUEST_SERVICE_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchGuestServices_TestEmpty_ExpectEmptyList(
      guest_service_provider_conn: sqlite3.Connection ) -> None:
   assert GuestServiceProvider.fetch_guest_services(
      guest_service_provider_conn ) == []


def Test_FetchGuestServices_TestPopulated_ExpectMappedFields(
      guest_service_provider_conn: sqlite3.Connection ) -> None:
   guest_service_provider_conn.execute(
      """   INSERT INTO GuestService (
               SERVICE_TYPE,
               X_COORD,
               Y_COORD
            )
            VALUES ( ?, ?, ? );
      """,
      ( FIRST_AID, 5.5, 6.5 ),
   )
   guest_service_provider_conn.commit()

   services = GuestServiceProvider.fetch_guest_services(
      guest_service_provider_conn )

   assert len( services ) == 1
   assert services[ 0 ].service_type == FIRST_AID
   assert services[ 0 ].x_coord == 5.5
   assert services[ 0 ].y_coord == 6.5
