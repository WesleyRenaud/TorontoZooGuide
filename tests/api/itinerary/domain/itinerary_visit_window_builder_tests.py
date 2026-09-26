from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from api.shared.enums import ItineraryEventType


VISIT_WINDOW_SCHEMA = """
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

ARRIVAL_TIME = '09:30 AM'
DEPARTURE_TIME = '05:00 PM'
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
CHEETAH_SPECIES = 'Cheetah'
CAROUSEL_NAME = 'Conservation Carousel'
RAINFOREST_NAME = 'African Rainforest'
ZOOMOBILE_NAME = 'Zoomobile'
SPLASH_NAME = 'Splash Island'

OUTSIDE_LION_START = '08:30 AM'
OUTSIDE_LION_END = '08:45 AM'
IN_WINDOW_ENCOUNTER_START = '08:45 AM'
IN_WINDOW_ENCOUNTER_END = '09:30 AM'

DEPARTURE_LION_START = '3:45 PM'
DEPARTURE_LION_END = '3:53 PM'
AFTER_DEPARTURE_CHEETAH_START = '4:30 PM'
AFTER_DEPARTURE_CHEETAH_END = '4:38 PM'
DEPARTURE_CAROUSEL_START = '4:00 PM'
DEPARTURE_CAROUSEL_END = '4:08 PM'
AFTER_DEPARTURE_LUNCH_START = '4:30 PM'
AFTER_DEPARTURE_LUNCH_END = '5:00 PM'
EARLY_DEPARTURE_TIME = '04:15 PM'

BEFORE_ARRIVAL_LUNCH_START = '9:00 AM'
BEFORE_ARRIVAL_LUNCH_END = '9:30 AM'
LATER_ARRIVAL_TIME = '10:15 AM'

LATER_LION_START = '10:00 AM'
LATER_LION_END = '10:08 AM'
LATER_CHEETAH_START = '10:30 AM'
LATER_CHEETAH_END = '10:38 AM'
LATER_CAROUSEL_START = '11:00 AM'
LATER_CAROUSEL_END = '11:15 AM'
LATER_ENCOUNTER_START = '9:45 AM'
LATER_ENCOUNTER_END = '10:30 AM'

OUTSIDE_SPLASH_START = '8:00 AM'
OUTSIDE_SPLASH_END = '8:30 AM'
OUTSIDE_ZOOMOBILE_START = '7:30 AM'
OUTSIDE_ZOOMOBILE_END = '8:00 AM'
EVENT_ARRIVAL_START = '7:00 AM'
EVENT_ARRIVAL_END = '7:15 AM'
EVENT_DEPARTURE_START = '6:00 PM'
EVENT_DEPARTURE_END = '6:15 PM'
IN_WINDOW_LUNCH_START = '12:00 PM'
IN_WINDOW_LUNCH_END = '12:30 PM'

IN_WINDOW_ZOOMOBILE_START = '11:00 AM'
IN_WINDOW_ZOOMOBILE_END = '11:30 AM'


def _seed_animal(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      start_time: str,
      end_time: str,
      enclosure_name: str | None = None ) -> None:
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
      ( species, exhibit, enclosure_name, start_time, end_time ) )


def _seed_encounter(
      conn: sqlite3.Connection,
      *,
      name: str,
      start_time: str,
      end_time: str ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( name, start_time, end_time ) )


def _seed_attraction(
      conn: sqlite3.Connection,
      *,
      name: str,
      start_time: str,
      end_time: str ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( name, start_time, end_time ) )


def _seed_transportation(
      conn: sqlite3.Connection,
      *,
      name: str,
      start_time: str,
      end_time: str ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ? );
      """,
      ( name, start_time, end_time ) )


def _seed_event(
      conn: sqlite3.Connection,
      *,
      event_type: str,
      start_time: str,
      end_time: str ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( event_type, start_time, end_time ) )


def _connect() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( VISIT_WINDOW_SCHEMA )
   return conn


def _fetch_times(
      conn: sqlite3.Connection,
      table: str,
      column: str,
      value: str ) -> sqlite3.Row | None:
   return conn.execute(
      f"""   SELECT START_TIME, END_TIME
            FROM { table }
            WHERE { column } = ?;
      """,
      ( value, ),
   ).fetchone()


def _event_start(
      conn: sqlite3.Connection,
      event_type: str ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT START_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( event_type, ),
   ).fetchone()


def _event_count(
      conn: sqlite3.Connection,
      event_type: str ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( event_type, ),
   ).fetchone()


@pytest.fixture
def visit_window_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_animal(
      conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=OUTSIDE_LION_START,
      end_time=OUTSIDE_LION_END )
   _seed_encounter(
      conn,
      name=RAINFOREST_NAME,
      start_time=IN_WINDOW_ENCOUNTER_START,
      end_time=IN_WINDOW_ENCOUNTER_END )
   conn.commit()
   yield conn
   conn.close()


@pytest.fixture
def departure_window_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_animal(
      conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=DEPARTURE_LION_START,
      end_time=DEPARTURE_LION_END )
   _seed_animal(
      conn,
      species=CHEETAH_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=AFTER_DEPARTURE_CHEETAH_START,
      end_time=AFTER_DEPARTURE_CHEETAH_END )
   _seed_attraction(
      conn,
      name=CAROUSEL_NAME,
      start_time=DEPARTURE_CAROUSEL_START,
      end_time=DEPARTURE_CAROUSEL_END )
   _seed_event(
      conn,
      event_type=ItineraryEventType.LUNCH.value,
      start_time=AFTER_DEPARTURE_LUNCH_START,
      end_time=AFTER_DEPARTURE_LUNCH_END )
   conn.commit()
   yield conn
   conn.close()


@pytest.fixture
def arrival_window_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_event(
      conn,
      event_type=ItineraryEventType.LUNCH.value,
      start_time=BEFORE_ARRIVAL_LUNCH_START,
      end_time=BEFORE_ARRIVAL_LUNCH_END )
   conn.commit()
   yield conn
   conn.close()


@pytest.fixture
def later_arrival_window_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_animal(
      conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=LATER_LION_START,
      end_time=LATER_LION_END )
   _seed_animal(
      conn,
      species=CHEETAH_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=LATER_CHEETAH_START,
      end_time=LATER_CHEETAH_END )
   _seed_attraction(
      conn,
      name=CAROUSEL_NAME,
      start_time=LATER_CAROUSEL_START,
      end_time=LATER_CAROUSEL_END )
   _seed_encounter(
      conn,
      name=RAINFOREST_NAME,
      start_time=LATER_ENCOUNTER_START,
      end_time=LATER_ENCOUNTER_END )
   conn.commit()
   yield conn
   conn.close()


@pytest.fixture
def outside_attraction_transport_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_attraction(
      conn,
      name=SPLASH_NAME,
      start_time=OUTSIDE_SPLASH_START,
      end_time=OUTSIDE_SPLASH_END )
   _seed_transportation(
      conn,
      name=ZOOMOBILE_NAME,
      start_time=OUTSIDE_ZOOMOBILE_START,
      end_time=OUTSIDE_ZOOMOBILE_END )
   _seed_event(
      conn,
      event_type=ItineraryEventType.ARRIVAL.value,
      start_time=EVENT_ARRIVAL_START,
      end_time=EVENT_ARRIVAL_END )
   _seed_event(
      conn,
      event_type=ItineraryEventType.DEPARTURE.value,
      start_time=EVENT_DEPARTURE_START,
      end_time=EVENT_DEPARTURE_END )
   _seed_event(
      conn,
      event_type=ItineraryEventType.LUNCH.value,
      start_time=IN_WINDOW_LUNCH_START,
      end_time=IN_WINDOW_LUNCH_END )
   conn.commit()
   yield conn
   conn.close()


@pytest.fixture
def in_window_transport_conn() -> sqlite3.Connection:
   conn = _connect()
   _seed_transportation(
      conn,
      name=ZOOMOBILE_NAME,
      start_time=IN_WINDOW_ZOOMOBILE_START,
      end_time=IN_WINDOW_ZOOMOBILE_END )
   conn.commit()
   yield conn
   conn.close()


def Test_ScheduleTimeOccursOutside_TestBeforeArrival_ExpectTrue() -> None:
   start_time = '9:00 AM'
   end_time = '9:30 AM'
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   occurs_outside = ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      start_time,
      end_time,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert occurs_outside is True


def Test_ScheduleTimeOccursOutside_TestAfterDeparture_ExpectTrue() -> None:
   start_time = '4:30 PM'
   end_time = '5:30 PM'
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   occurs_outside = ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      start_time,
      end_time,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert occurs_outside is True


def Test_ScheduleTimeOccursOutside_TestInsideWindow_ExpectFalse() -> None:
   start_time = '11:00 AM'
   end_time = '11:30 AM'
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   occurs_outside = ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      start_time,
      end_time,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert occurs_outside is False


def Test_ClearedScheduleTimes_TestOutsideWindow_ExpectCleared() -> None:
   start_time = '9:00 AM'
   end_time = '9:30 AM'
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   cleared = ItineraryVisitWindowBuilder.cleared_schedule_times(
      start_time,
      end_time,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert cleared == ( None, None )


def Test_ClearedScheduleTimes_TestInsideWindow_ExpectUnchanged() -> None:
   start_time = '11:00 AM'
   end_time = '11:30 AM'
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   cleared = ItineraryVisitWindowBuilder.cleared_schedule_times(
      start_time,
      end_time,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert cleared == ( start_time, end_time )


def Test_ClearSchedulesOutside_TestOutsideAnimal_ExpectClearedAnimalOnly(
      visit_window_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      visit_window_conn,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   animal = visit_window_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( LION_SPECIES, LION_EXHIBIT ),
   ).fetchone()
   encounter = _fetch_times(
      visit_window_conn,
      'ItineraryWildEncounter',
      'WILD_ENCOUNTER',
      RAINFOREST_NAME )

   assert did_clear is True
   assert animal is not None
   assert animal[ 'START_TIME' ] is None
   assert animal[ 'END_TIME' ] is None
   assert encounter is not None
   assert encounter[ 'START_TIME' ] == IN_WINDOW_ENCOUNTER_START
   assert encounter[ 'END_TIME' ] == IN_WINDOW_ENCOUNTER_END


def Test_ClearSchedulesOutside_TestAfterDepartureAnimal_ExpectClearedCheetahOnly(
      departure_window_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      departure_window_conn,
      arrival_time=ARRIVAL_TIME,
      departure_time=EARLY_DEPARTURE_TIME )

   lion = _fetch_times(
      departure_window_conn,
      'ItineraryAnimal',
      'SPECIES',
      LION_SPECIES )
   cheetah = _fetch_times(
      departure_window_conn,
      'ItineraryAnimal',
      'SPECIES',
      CHEETAH_SPECIES )
   carousel = _fetch_times(
      departure_window_conn,
      'ItineraryAttraction',
      'ATTRACTION',
      CAROUSEL_NAME )
   lunch_count = _event_count(
      departure_window_conn,
      ItineraryEventType.LUNCH.value )

   assert did_clear is True
   assert lion is not None
   assert lion[ 'START_TIME' ] == DEPARTURE_LION_START
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] is None
   assert carousel is not None
   assert carousel[ 'START_TIME' ] == DEPARTURE_CAROUSEL_START
   assert lunch_count is not None
   assert lunch_count[ 'COUNT' ] == 0


def Test_ClearSchedulesOutside_TestBeforeArrivalEvent_ExpectLunchDeleted(
      arrival_window_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      arrival_window_conn,
      arrival_time=LATER_ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   lunch_count = _event_count(
      arrival_window_conn,
      ItineraryEventType.LUNCH.value )

   assert did_clear is True
   assert lunch_count is not None
   assert lunch_count[ 'COUNT' ] == 0


def Test_ClearSchedulesOutside_TestLaterArrival_ExpectBeforeArrivalAnimalCleared(
      later_arrival_window_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      later_arrival_window_conn,
      arrival_time=LATER_ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   lion = _fetch_times(
      later_arrival_window_conn,
      'ItineraryAnimal',
      'SPECIES',
      LION_SPECIES )
   cheetah = _fetch_times(
      later_arrival_window_conn,
      'ItineraryAnimal',
      'SPECIES',
      CHEETAH_SPECIES )
   carousel = _fetch_times(
      later_arrival_window_conn,
      'ItineraryAttraction',
      'ATTRACTION',
      CAROUSEL_NAME )
   encounter = _fetch_times(
      later_arrival_window_conn,
      'ItineraryWildEncounter',
      'WILD_ENCOUNTER',
      RAINFOREST_NAME )

   assert did_clear is True
   assert lion is not None
   assert lion[ 'START_TIME' ] is None
   assert lion[ 'END_TIME' ] is None
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == LATER_CHEETAH_START
   assert carousel is not None
   assert carousel[ 'START_TIME' ] == LATER_CAROUSEL_START
   assert encounter is not None
   assert encounter[ 'START_TIME' ] == LATER_ENCOUNTER_START


def Test_ClearSchedulesOutside_TestOutsideAttractionAndTransport_ExpectCleared(
      outside_attraction_transport_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      outside_attraction_transport_conn,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   splash = _fetch_times(
      outside_attraction_transport_conn,
      'ItineraryAttraction',
      'ATTRACTION',
      SPLASH_NAME )
   zoomobile = _fetch_times(
      outside_attraction_transport_conn,
      'ItineraryTransportation',
      'TRANSPORTATION',
      ZOOMOBILE_NAME )
   arrival = _event_start(
      outside_attraction_transport_conn,
      ItineraryEventType.ARRIVAL.value )
   departure = _event_start(
      outside_attraction_transport_conn,
      ItineraryEventType.DEPARTURE.value )
   lunch = _event_start(
      outside_attraction_transport_conn,
      ItineraryEventType.LUNCH.value )

   assert did_clear is True
   assert splash is not None
   assert splash[ 'START_TIME' ] is None
   assert zoomobile is not None
   assert zoomobile[ 'START_TIME' ] is None
   assert arrival is not None
   assert arrival[ 'START_TIME' ] == EVENT_ARRIVAL_START
   assert departure is not None
   assert departure[ 'START_TIME' ] == EVENT_DEPARTURE_START
   assert lunch is not None
   assert lunch[ 'START_TIME' ] == IN_WINDOW_LUNCH_START


def Test_ClearSchedulesOutside_TestInWindowTransportation_ExpectKept(
      in_window_transport_conn: sqlite3.Connection ) -> None:
   did_clear = ItineraryVisitWindowBuilder.clear_schedules_outside(
      in_window_transport_conn,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   zoomobile = _fetch_times(
      in_window_transport_conn,
      'ItineraryTransportation',
      'TRANSPORTATION',
      ZOOMOBILE_NAME )

   assert did_clear is False
   assert zoomobile is not None
   assert zoomobile[ 'START_TIME' ] == IN_WINDOW_ZOOMOBILE_START
