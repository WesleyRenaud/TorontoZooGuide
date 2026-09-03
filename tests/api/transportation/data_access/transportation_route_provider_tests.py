from __future__ import annotations

import sqlite3

import pytest

from api.transportation.data_access.transportation_route_provider import TransportationRouteProvider

TRANSPORTATION_ROUTE_PROVIDER_SCHEMA = """
CREATE TABLE Transportation (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   IS_ALSO_ATTRACTION   INTEGER NOT NULL
);

CREATE TABLE TransportationRoute (
   TRANSPORTATION   TEXT NOT NULL,
   ROUTE            TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ROUTE )
);
"""

ZOOMOBILE = 'Zoomobile'

@pytest.fixture
def transportation_route_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_ROUTE_PROVIDER_SCHEMA )

   yield conn

   conn.close()

def Test_FetchTransportationRoutesByName_TestEmpty_ExpectEmptyList(
      transportation_route_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationRouteProvider.fetch_transportation_routes_by_name(
      transportation_route_provider_conn ) == []

def Test_FetchTransportationRoutesByName_TestPopulated_ExpectMappedRoutes(
      transportation_route_provider_conn: sqlite3.Connection ) -> None:
   transportation_route_provider_conn.execute(
      """   INSERT INTO Transportation (
               NAME,
               IS_ALSO_ATTRACTION
            )
            VALUES ( ?, 1 );
      """,
      ( ZOOMOBILE, ),
   )
   transportation_route_provider_conn.execute(
      """   INSERT INTO TransportationRoute (
               TRANSPORTATION,
               ROUTE
            )
            VALUES ( ?, ? ), ( ?, ? );
      """,
      ( ZOOMOBILE, 'summer', ZOOMOBILE, 'winter' ),
   )
   transportation_route_provider_conn.commit()

   routes = TransportationRouteProvider.fetch_transportation_routes_by_name(
      transportation_route_provider_conn )

   assert [ ( route.transportation, route.route ) for route in routes ] == [
      ( ZOOMOBILE, 'summer' ),
      ( ZOOMOBILE, 'winter' ),
   ]
