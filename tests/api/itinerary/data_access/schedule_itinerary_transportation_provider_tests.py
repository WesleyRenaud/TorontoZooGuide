from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from api.itinerary.data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
SUMMER_ROUTE = 'summer'
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

CREATE TABLE ItineraryAnimal (
   SPECIES                 TEXT        NOT NULL,
   EXHIBIT                 TEXT        NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER     NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER     NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT
);

CREATE TABLE TransportationAnimal (
   TRANSPORTATION      TEXT        NOT NULL,
   FROM_STATION        TEXT        NOT NULL,
   TO_STATION          TEXT        NOT NULL,
   SPECIES             TEXT        NOT NULL,
   EXHIBIT             TEXT        NOT NULL,
   ENCLOSURE_NAME      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, ENCLOSURE_NAME )
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
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   start_time = '10:00 AM'
   route = SUMMER_ROUTE
   first_sequence_markers = [ 'm-a', 'm-b' ]
   second_sequence_markers = [ 'm-c' ]
   route_marker_sequences = [ first_sequence_markers, second_sequence_markers ]
   total_duration_minutes = sum(
      segment.duration_minutes for segment in SUMMER_ROUTE_LEG_SEGMENTS )
   end_time = DateValues.add_minutes_to_time( start_time, total_duration_minutes )
   cur = schedule_transportation_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=added_as_attraction )
   schedule_transportation_conn.commit()
   cur.close()
   monkeypatch.setattr(
      'api.itinerary.data_access.schedule_itinerary_transportation_provider.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: route_marker_sequences )

   cur = schedule_transportation_conn.cursor()
   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
      cur,
      name=transportation,
      added_as_attraction=added_as_attraction,
      start_time=start_time,
      route=route,
      legs=SUMMER_ROUTE_LEG_SEGMENTS )
   schedule_transportation_conn.commit()
   cur.close()
   persisted = schedule_transportation_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( transportation, ),
   ).fetchone()
   legs = schedule_transportation_conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1
            ORDER BY START_TIME;
      """,
      ( transportation, ),
   ).fetchall()
   markers = ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      schedule_transportation_conn )

   assert applied is True
   assert persisted is not None
   assert persisted[ 'START_TIME' ] == start_time
   assert persisted[ 'END_TIME' ] == end_time
   assert persisted[ 'ROUTE' ] == route
   assert len( legs ) == len( SUMMER_ROUTE_LEG_SEGMENTS )
   assert legs[ Position.FIRST ][ 'FROM_STATION' ] == MAIN
   assert legs[ Position.LAST ][ 'TO_STATION' ] == MAIN
   assert { marker.sequence for marker in markers } == {
      Position.FIRST,
      Position.SECOND,
   }
   assert len( markers ) == sum(
      len( sequence ) for sequence in route_marker_sequences )


def Test_ApplyItineraryTransportationSchedule_TestDiscontinuousLegs_ExpectSplitMarkerSequences(
      schedule_transportation_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   start_time = '10:00 AM'
   first_sequence_markers = [ 'm-a', 'm-b' ]
   second_sequence_markers = [ 'm-d', 'm-e' ]
   route_marker_sequences = [ first_sequence_markers, second_sequence_markers ]
   legs = [
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
   ]
   cur = schedule_transportation_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=added_as_attraction )
   schedule_transportation_conn.commit()
   cur.close()
   monkeypatch.setattr(
      'api.itinerary.data_access.schedule_itinerary_transportation_provider.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: route_marker_sequences )

   cur = schedule_transportation_conn.cursor()
   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
      cur,
      name=transportation,
      added_as_attraction=added_as_attraction,
      start_time=start_time,
      route=SUMMER_ROUTE,
      legs=legs )
   schedule_transportation_conn.commit()
   cur.close()
   markers = ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers(
      schedule_transportation_conn )

   assert applied is True
   assert { marker.sequence for marker in markers } == {
      Position.FIRST,
      Position.SECOND,
   }
   assert [
      marker.marker_id
      for marker in markers
      if marker.sequence == Position.FIRST
   ] == first_sequence_markers
   assert [
      marker.marker_id
      for marker in markers
      if marker.sequence == Position.SECOND
   ] == second_sequence_markers


def Test_ApplyItineraryTransportationRideSegments_TestEmptySegments_ExpectFalse(
      schedule_transportation_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   segments = []
   cur = schedule_transportation_conn.cursor()

   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments(
      cur,
      name=transportation,
      added_as_attraction=added_as_attraction,
      route=SUMMER_ROUTE,
      segments=segments )
   cur.close()

   assert not applied


def Test_ApplyItineraryTransportationRideSegments_TestEmptyLegs_ExpectFalse(
      schedule_transportation_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   start_time = '10:00 AM'
   segments = [ ( start_time, [] ) ]
   cur = schedule_transportation_conn.cursor()

   applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments(
      cur,
      name=transportation,
      added_as_attraction=added_as_attraction,
      route=SUMMER_ROUTE,
      segments=segments )
   cur.close()

   assert not applied
