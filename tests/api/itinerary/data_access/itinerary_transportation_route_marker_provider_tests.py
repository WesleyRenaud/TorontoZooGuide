from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider


ZOOMOBILE = 'Zoomobile'

ROUTE_MARKER_SCHEMA = """
CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER     NOT NULL,
   MARKER_ORDER             INTEGER     NOT NULL,
   MARKER_ID                TEXT        NOT NULL
);
"""


@pytest.fixture
def route_marker_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ROUTE_MARKER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_InsertItineraryTransportationRouteMarkers_TestSequences_ExpectOrderedRecords(
      route_marker_conn: sqlite3.Connection ) -> None:
   cur = route_marker_conn.cursor()
   ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      route_marker_sequences=[
         [ 'm-a', 'm-b' ],
         [ 'm-c' ],
      ] )
   route_marker_conn.commit()
   cur.close()

   markers = ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      route_marker_conn )

   assert len( markers ) == 3
   assert markers[ 0 ].sequence == 0
   assert markers[ 0 ].marker_order == 0
   assert markers[ 0 ].marker_id == 'm-a'
   assert markers[ 2 ].sequence == 1
   assert markers[ 2 ].marker_id == 'm-c'


def Test_DeleteItineraryTransportationRouteMarkers_TestOwnedRows_ExpectRemoved(
      route_marker_conn: sqlite3.Connection ) -> None:
   cur = route_marker_conn.cursor()
   ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      route_marker_sequences=[ [ 'm-a' ] ] )
   ItineraryTransportationRouteMarkerProvider.delete_itinerary_transportation_route_markers(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True )
   route_marker_conn.commit()
   cur.close()

   assert ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      route_marker_conn ) == []


def Test_ClearItineraryTransportationRouteMarkers_TestOwnedRows_ExpectEmptyTable(
      route_marker_conn: sqlite3.Connection ) -> None:
   cur = route_marker_conn.cursor()
   ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      route_marker_sequences=[ [ 'm-a' ] ] )
   ItineraryTransportationRouteMarkerProvider.clear_itinerary_transportation_route_markers( cur )
   route_marker_conn.commit()
   cur.close()

   assert route_marker_conn.execute(
      'SELECT COUNT(*) FROM ItineraryTransportationRouteMarker;' ).fetchone()[ 0 ] == 0
