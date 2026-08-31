from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder


VISIT_WINDOW_SCHEMA = """
CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT        NOT NULL,
   EXHIBIT              TEXT        NOT NULL,
   ENCLOSURE_NAME       TEXT,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK      INTEGER     NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT        NOT NULL,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

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

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);
"""


@pytest.fixture
def visit_window_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( VISIT_WINDOW_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', '08:30 AM', '08:45 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( 'African Rainforest', '08:45 AM', '09:30 AM' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_ScheduleTimeOccursOutside_TestBeforeArrival_ExpectTrue() -> None:
   assert ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '9:00 AM',
      '9:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ScheduleTimeOccursOutside_TestAfterDeparture_ExpectTrue() -> None:
   assert ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '4:30 PM',
      '5:30 PM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ScheduleTimeOccursOutside_TestInsideWindow_ExpectFalse() -> None:
   assert not ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '11:00 AM',
      '11:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ClearedScheduleTimes_TestOutsideWindow_ExpectCleared() -> None:
   assert ItineraryVisitWindowBuilder.cleared_schedule_times(
      '9:00 AM',
      '9:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' ) == ( None, None )


def Test_ClearedScheduleTimes_TestInsideWindow_ExpectUnchanged() -> None:
   assert ItineraryVisitWindowBuilder.cleared_schedule_times(
      '11:00 AM',
      '11:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' ) == ( '11:00 AM', '11:30 AM' )


def Test_ClearSchedulesOutside_TestOutsideAnimal_ExpectClearedAnimalOnly(
      visit_window_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      visit_window_conn,
      arrival_time='09:30 AM',
      departure_time='05:00 PM' )

   animal = visit_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()
   encounter = visit_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( 'African Rainforest', ),
   ).fetchone()

   assert animal is not None
   assert animal[ 'START_TIME' ] is None
   assert animal[ 'END_TIME' ] is None
   assert encounter is not None
   assert encounter[ 'START_TIME' ] == '08:45 AM'
   assert encounter[ 'END_TIME' ] == '09:30 AM'
