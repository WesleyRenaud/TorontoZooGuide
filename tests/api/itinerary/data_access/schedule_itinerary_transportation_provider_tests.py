from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from api.itinerary.data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'

SUMMER_ROUTE_LEG_SEGMENTS = [
   TransportationRouteLegSegment( MAIN, CANADA, 20 ),
   TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
   TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
   TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
   TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
]

SCHEDULE_TRANSPORTATION_SCHEMA = """
CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   START_TIME               TEXT        NOT NULL,
   END_TIME                 TEXT        NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER     NOT NULL,
   MARKER_ORDER             INTEGER     NOT NULL,
   MARKER_ID                TEXT        NOT NULL
);
"""


@pytest.fixture
def schedule_transportation_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEDULE_TRANSPORTATION_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_ApplyItineraryTransportationSchedule_TestSummerLoop_ExpectTimedLegsAndRoute(
      schedule_transportation_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   cur = schedule_transportation_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=True )
   schedule_transportation_conn.commit()
   cur.close()

   monkeypatch.setattr(
      'api.itinerary.data_access.schedule_itinerary_transportation_provider.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: [
         [ 'm-a', 'm-b' ],
         [ 'm-c' ],
      ] )

   cur = schedule_transportation_conn.cursor()
   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
      cur,
      name=ZOOMOBILE,
      added_as_attraction=True,
      start_time='10:00 AM',
      route='summer',
      legs=SUMMER_ROUTE_LEG_SEGMENTS )
   schedule_transportation_conn.commit()
   cur.close()

   assert applied is True

   transportation = schedule_transportation_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   legs = schedule_transportation_conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1
            ORDER BY START_TIME;
      """,
      ( ZOOMOBILE, ),
   ).fetchall()
   markers = ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      schedule_transportation_conn )

   assert transportation is not None
   assert transportation[ 'START_TIME' ] == '10:00 AM'
   assert transportation[ 'END_TIME' ] == '11:15 AM'
   assert transportation[ 'ROUTE' ] == 'summer'
   assert len( legs ) == 5
   assert legs[ 0 ][ 'FROM_STATION' ] == MAIN
   assert legs[ -1 ][ 'TO_STATION' ] == MAIN
   assert { marker.sequence for marker in markers } == { 0, 1 }
   assert len( markers ) == 3


def Test_ApplyItineraryTransportationSchedule_TestDiscontinuousLegs_ExpectSplitMarkerSequences(
      schedule_transportation_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   cur = schedule_transportation_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=True )
   schedule_transportation_conn.commit()
   cur.close()

   monkeypatch.setattr(
      'api.itinerary.data_access.schedule_itinerary_transportation_provider.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: [
         [ 'm-a', 'm-b' ],
         [ 'm-d', 'm-e' ],
      ] )

   cur = schedule_transportation_conn.cursor()
   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
      cur,
      name=ZOOMOBILE,
      added_as_attraction=True,
      start_time='10:00 AM',
      route='summer',
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
         TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
      ] )
   schedule_transportation_conn.commit()
   cur.close()

   assert applied is True

   markers = ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      schedule_transportation_conn )

   assert { marker.sequence for marker in markers } == { 0, 1 }
   assert [ marker.marker_id for marker in markers if marker.sequence == 0 ] == [ 'm-a', 'm-b' ]
   assert [ marker.marker_id for marker in markers if marker.sequence == 1 ] == [ 'm-d', 'm-e' ]
