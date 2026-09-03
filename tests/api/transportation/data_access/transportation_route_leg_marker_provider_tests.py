from __future__ import annotations

import sqlite3

import pytest

from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider
from api.transportation.data_access.transportation_route_leg_marker_record import TransportationRouteLegMarkerRecord

ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
SUMMER_ROUTE = 'summer'
MARKER_MAXIMUM = 297

TRANSPORTATION_ROUTE_LEG_MARKER_SCHEMA = """
CREATE TABLE TransportationRouteLegMarker (
   TRANSPORTATION     TEXT NOT NULL,
   ROUTE              TEXT NOT NULL,
   FROM_STATION       TEXT NOT NULL,
   TO_STATION         TEXT NOT NULL,
   MARKER_ID          TEXT NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ROUTE, FROM_STATION, TO_STATION, MARKER_ID )
);
"""


def ordered_marker_ids(
      prefix: str,
      start: int,
      end: int,
      maximum: int ) -> list[ str ]:
   marker_numbers = (
      range( start, end + 1 )
      if start <= end
      else [ *range( start, maximum + 1 ), *range( 1, end + 1 ) ]
   )

   return [
      f'{ prefix }-{ str( marker_number ).zfill( 3 ) }'
      for marker_number in marker_numbers
   ]


MAIN_TO_CANADA_MARKERS = ordered_marker_ids( 'zm-s', 5, 85, MARKER_MAXIMUM )
EURASIA_TO_MAIN_MARKERS = ordered_marker_ids( 'zm-s', 252, 4, MARKER_MAXIMUM )

@pytest.fixture
def leg_marker_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_ROUTE_LEG_MARKER_SCHEMA )

   yield conn

   conn.close()


def _insert_marker(
      conn: sqlite3.Connection,
      *,
      from_station: str,
      to_station: str,
      marker_id: str ) -> None:
   conn.execute(
      """   INSERT INTO TransportationRouteLegMarker (
               TRANSPORTATION,
               ROUTE,
               FROM_STATION,
               TO_STATION,
               MARKER_ID
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, SUMMER_ROUTE, from_station, to_station, marker_id ),
   )


def Test_MarkersByLegForMarkers_TestRecords_ExpectGroupedByStations() -> None:
   markers = [
      TransportationRouteLegMarkerRecord(
         from_station=MAIN,
         to_station=CANADA,
         marker_id='zm-s-005' ),
      TransportationRouteLegMarkerRecord(
         from_station=MAIN,
         to_station=CANADA,
         marker_id='zm-s-006' ),
      TransportationRouteLegMarkerRecord(
         from_station=EURASIA,
         to_station=MAIN,
         marker_id='zm-s-252' ),
   ]

   assert TransportationRouteLegMarkerProvider.markers_by_leg_for_markers(
      markers ) == {
         ( MAIN, CANADA ): [ 'zm-s-005', 'zm-s-006' ],
         ( EURASIA, MAIN ): [ 'zm-s-252' ],
      }


def Test_FetchTransportationRouteLegMarkersByLeg_TestInsertedRows_ExpectTravelOrder(
      leg_marker_conn: sqlite3.Connection ) -> None:
   for marker_id in MAIN_TO_CANADA_MARKERS[ :3 ]:
      _insert_marker(
         leg_marker_conn,
         from_station=MAIN,
         to_station=CANADA,
         marker_id=marker_id )
   for marker_id in EURASIA_TO_MAIN_MARKERS[ :2 ]:
      _insert_marker(
         leg_marker_conn,
         from_station=EURASIA,
         to_station=MAIN,
         marker_id=marker_id )

   markers_by_leg = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_markers_by_leg(
      leg_marker_conn,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE )

   assert markers_by_leg[ ( MAIN, CANADA ) ] == MAIN_TO_CANADA_MARKERS[ :3 ]
   assert markers_by_leg[ ( EURASIA, MAIN ) ] == EURASIA_TO_MAIN_MARKERS[ :2 ]


def Test_FetchTransportationRouteLegMarkerIds_TestEmptyLegs_ExpectEmptyList(
      leg_marker_conn: sqlite3.Connection ) -> None:
   assert TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      leg_marker_conn,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE,
      legs=[] ) == []


def Test_FetchTransportationRouteLegMarkerIds_TestSingleLeg_ExpectTravelOrder(
      leg_marker_conn: sqlite3.Connection ) -> None:
   for marker_id in MAIN_TO_CANADA_MARKERS[ :4 ]:
      _insert_marker(
         leg_marker_conn,
         from_station=MAIN,
         to_station=CANADA,
         marker_id=marker_id )

   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      leg_marker_conn,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == MAIN_TO_CANADA_MARKERS[ :4 ]


def Test_FetchTransportationRouteLegMarkerIds_TestWraparoundLeg_ExpectTravelOrder(
      leg_marker_conn: sqlite3.Connection ) -> None:
   for marker_id in EURASIA_TO_MAIN_MARKERS[ :3 ]:
      _insert_marker(
         leg_marker_conn,
         from_station=EURASIA,
         to_station=MAIN,
         marker_id=marker_id )

   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      leg_marker_conn,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=EURASIA,
            to_station=MAIN,
            start_time='11:00 AM',
            end_time='11:15 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == EURASIA_TO_MAIN_MARKERS[ :3 ]
   assert marker_ids_result[ 0 ] == 'zm-s-252'
