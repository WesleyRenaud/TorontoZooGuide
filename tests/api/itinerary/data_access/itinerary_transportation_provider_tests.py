from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'

TRANSPORTATION_PROVIDER_SCHEMA = """
CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0,
   PRIMARY KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION )
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
def transportation_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_InsertItineraryTransportation_TestNewRow_ExpectInserted(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   inserted = ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time='10:00 AM',
      end_time='11:15 AM',
      route='summer' )
   transportation_provider_conn.commit()
   cur.close()

   row = transportation_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert inserted is True
   assert row is not None
   assert row[ 'START_TIME' ] == '10:00 AM'
   assert row[ 'END_TIME' ] == '11:15 AM'
   assert row[ 'ROUTE' ] == 'summer'
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_InsertItineraryTransportation_TestDuplicateRow_ExpectIgnored(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True )
   duplicate_inserted = ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=50,
      added_as_attraction=True )
   transportation_provider_conn.commit()
   cur.close()

   row = transportation_provider_conn.execute(
      """   SELECT NEW_LIKELIHOOD
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert duplicate_inserted is False
   assert row is not None
   assert row[ 'NEW_LIKELIHOOD' ] == 100


def Test_InsertItineraryTransportationLegs_TestLegs_ExpectPersistedRows(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation_legs(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=True ),
      ] )
   transportation_provider_conn.commit()
   cur.close()

   legs = transportation_provider_conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchall()

   assert len( legs ) == 1
   assert legs[ 0 ][ 'FROM_STATION' ] == MAIN
   assert legs[ 0 ][ 'TO_STATION' ] == CANADA


def Test_ClearItineraryTransportationScheduleTimes_TestScheduledRow_ExpectClearedFields(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time='10:00 AM',
      end_time='11:15 AM',
      route='summer',
      bulk_transit_evaluated=True )
   ItineraryTransportationProvider.clear_itinerary_transportation_schedule_times(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True )
   transportation_provider_conn.commit()
   cur.close()

   row = transportation_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None
   assert row[ 'ROUTE' ] is None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_SetItineraryTransportationBulkTransitEvaluated_TestRow_ExpectUpdatedFlag(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True )
   ItineraryTransportationProvider.set_itinerary_transportation_bulk_transit_evaluated(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      bulk_transit_evaluated=True )
   transportation_provider_conn.commit()
   cur.close()

   row = transportation_provider_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 1


def Test_DeleteItineraryTransportation_TestScheduledRow_ExpectRowLegsAndMarkersRemoved(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True )
   ItineraryTransportationProvider.insert_itinerary_transportation_legs(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=True ),
      ] )
   ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      route_marker_sequences=[ [ 'm-a', 'm-b' ] ] )
   ItineraryTransportationProvider.delete_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      added_as_attraction=True )
   transportation_provider_conn.commit()
   cur.close()

   transportation_count = transportation_provider_conn.execute(
      'SELECT COUNT(*) FROM ItineraryTransportation;' ).fetchone()[ 0 ]
   leg_count = transportation_provider_conn.execute(
      'SELECT COUNT(*) FROM ItineraryTransportationLeg;' ).fetchone()[ 0 ]
   marker_count = transportation_provider_conn.execute(
      'SELECT COUNT(*) FROM ItineraryTransportationRouteMarker;' ).fetchone()[ 0 ]

   assert transportation_count == 0
   assert leg_count == 0
   assert marker_count == 0


def Test_ClearAllItineraryTransportationScheduleTimes_TestScheduledRows_ExpectAllCleared(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   cur = transportation_provider_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time='10:00 AM',
      end_time='11:15 AM',
      route='summer' )
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=False,
      start_time='11:30 AM',
      end_time='12:00 PM',
      route='transit' )
   ItineraryTransportationProvider.clear_all_itinerary_transportation_schedule_times( cur )
   transportation_provider_conn.commit()
   cur.close()

   rows = transportation_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            ORDER BY ADDED_AS_ATTRACTION;
      """,
   ).fetchall()

   assert len( rows ) == 2
   assert all( row[ 'START_TIME' ] is None for row in rows )
   assert all( row[ 'END_TIME' ] is None for row in rows )
   assert all( row[ 'ROUTE' ] is None for row in rows )
   assert all( row[ 'BULK_TRANSIT_EVALUATED' ] == 0 for row in rows )
