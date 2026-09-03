from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from api.shared.enums import ItineraryEventType


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


@pytest.fixture
def departure_window_conn() -> sqlite3.Connection:
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
      ( 'African Lion', 'Africa Savanna', '3:45 PM', '3:53 PM' ) )
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
      ( 'Cheetah', 'Africa Savanna', '4:30 PM', '4:38 PM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'Conservation Carousel', '4:00 PM', '4:08 PM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '4:30 PM', '5:00 PM' ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def arrival_window_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( VISIT_WINDOW_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '9:00 AM', '9:30 AM' ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def later_arrival_window_conn() -> sqlite3.Connection:
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
      ( 'African Lion', 'Africa Savanna', '10:00 AM', '10:08 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', None, '10:30 AM', '10:38 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'Conservation Carousel', '11:00 AM', '11:15 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( 'African Rainforest', '9:45 AM', '10:30 AM' ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def outside_attraction_transport_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( VISIT_WINDOW_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'Splash Island', '8:00 AM', '8:30 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ? );
      """,
      ( 'Zoomobile', '7:30 AM', '8:00 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.ARRIVAL.value, '7:00 AM', '7:15 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.DEPARTURE.value, '6:00 PM', '6:15 PM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:00 PM', '12:30 PM' ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def in_window_transport_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( VISIT_WINDOW_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ? );
      """,
      ( 'Zoomobile', '11:00 AM', '11:30 AM' ) )
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


def Test_ClearSchedulesOutside_TestAfterDepartureAnimal_ExpectClearedCheetahOnly(
      departure_window_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      departure_window_conn,
      arrival_time='09:30 AM',
      departure_time='04:15 PM' )

   lion = departure_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'African Lion', ),
   ).fetchone()
   cheetah = departure_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'Cheetah', ),
   ).fetchone()
   carousel = departure_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()
   lunch_count = departure_window_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.LUNCH.value, ),
   ).fetchone()

   assert lion is not None
   assert lion[ 'START_TIME' ] == '3:45 PM'
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] is None
   assert carousel is not None
   assert carousel[ 'START_TIME' ] == '4:00 PM'
   assert lunch_count is not None
   assert lunch_count[ 'COUNT' ] == 0


def Test_ClearSchedulesOutside_TestBeforeArrivalEvent_ExpectLunchDeleted(
      arrival_window_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      arrival_window_conn,
      arrival_time='10:15 AM',
      departure_time='05:00 PM' )

   lunch_count = arrival_window_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.LUNCH.value, ),
   ).fetchone()

   assert lunch_count is not None
   assert lunch_count[ 'COUNT' ] == 0


def Test_ClearSchedulesOutside_TestLaterArrival_ExpectBeforeArrivalAnimalCleared(
      later_arrival_window_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      later_arrival_window_conn,
      arrival_time='10:15 AM',
      departure_time='05:00 PM' )

   lion = later_arrival_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'African Lion', ),
   ).fetchone()
   cheetah = later_arrival_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'Cheetah', ),
   ).fetchone()
   carousel = later_arrival_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()
   encounter = later_arrival_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( 'African Rainforest', ),
   ).fetchone()

   assert lion is not None
   assert lion[ 'START_TIME' ] is None
   assert lion[ 'END_TIME' ] is None
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '10:30 AM'
   assert carousel is not None
   assert carousel[ 'START_TIME' ] == '11:00 AM'
   assert encounter is not None
   assert encounter[ 'START_TIME' ] == '9:45 AM'


def Test_ClearSchedulesOutside_TestOutsideAttractionAndTransport_ExpectCleared(
      outside_attraction_transport_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      outside_attraction_transport_conn,
      arrival_time='09:30 AM',
      departure_time='05:00 PM' )

   splash = outside_attraction_transport_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Splash Island', ),
   ).fetchone()
   zoomobile = outside_attraction_transport_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( 'Zoomobile', ),
   ).fetchone()
   arrival = outside_attraction_transport_conn.execute(
      """   SELECT START_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.ARRIVAL.value, ),
   ).fetchone()
   departure = outside_attraction_transport_conn.execute(
      """   SELECT START_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.DEPARTURE.value, ),
   ).fetchone()
   lunch = outside_attraction_transport_conn.execute(
      """   SELECT START_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.LUNCH.value, ),
   ).fetchone()

   assert splash is not None
   assert splash[ 'START_TIME' ] is None
   assert zoomobile is not None
   assert zoomobile[ 'START_TIME' ] is None
   assert arrival is not None
   assert arrival[ 'START_TIME' ] == '7:00 AM'
   assert departure is not None
   assert departure[ 'START_TIME' ] == '6:00 PM'
   assert lunch is not None
   assert lunch[ 'START_TIME' ] == '12:00 PM'


def Test_ClearSchedulesOutside_TestInWindowTransportation_ExpectKept(
      in_window_transport_conn: sqlite3.Connection ) -> None:
   ItineraryVisitWindowBuilder.clear_schedules_outside(
      in_window_transport_conn,
      arrival_time='09:30 AM',
      departure_time='05:00 PM' )

   zoomobile = in_window_transport_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( 'Zoomobile', ),
   ).fetchone()

   assert zoomobile is not None
   assert zoomobile[ 'START_TIME' ] == '11:00 AM'
