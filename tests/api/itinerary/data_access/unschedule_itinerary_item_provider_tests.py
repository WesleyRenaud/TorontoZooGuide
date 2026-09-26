from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from api.shared.date_values import DateValues
from api.shared.enums import ItineraryEventType, Position
from api.shared.enums.transportation_name import TransportationName


UNSCHEDULE_SCHEMA = """
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

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
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

GUARDIANS_SCHEMA = """
CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME TEXT NOT NULL PRIMARY KEY,
   START_TIME TEXT,
   END_TIME TEXT,
   IS_DELETED INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER TEXT NOT NULL,
   START_TIME TEXT NOT NULL,
   END_TIME TEXT,
   IS_DELETED INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY ( WILD_ENCOUNTER, START_TIME )
);
"""

CAROUSEL = 'Conservation Carousel'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
LION_TALK = 'African Lion'
RHINO_ENCOUNTER = 'White Rhinoceros'
LION_START_TIME = '10:00'
LION_DURATION_MINUTES = 8
LION_END_TIME = DateValues.add_minutes_to_time(
   LION_START_TIME,
   LION_DURATION_MINUTES )
CAROUSEL_START_TIME = '11:00'
CAROUSEL_DURATION_MINUTES = 20
CAROUSEL_END_TIME = DateValues.add_minutes_to_time(
   CAROUSEL_START_TIME,
   CAROUSEL_DURATION_MINUTES )
LUNCH_START_TIME = '12:00'
LUNCH_DURATION_MINUTES = 40
LUNCH_END_TIME = DateValues.add_minutes_to_time(
   LUNCH_START_TIME,
   LUNCH_DURATION_MINUTES )
ZOOMOBILE_START_TIME = '10:00 AM'
ZOOMOBILE_DURATION_MINUTES = 75
ZOOMOBILE_END_TIME = DateValues.add_minutes_to_time(
   ZOOMOBILE_START_TIME,
   ZOOMOBILE_DURATION_MINUTES )
LEG_DURATION_MINUTES = 20
TALK_START_TIME = '10:00 AM'
TALK_DURATION_MINUTES = 30
TALK_END_TIME = DateValues.add_minutes_to_time(
   TALK_START_TIME,
   TALK_DURATION_MINUTES )
ENCOUNTER_START_TIME = '1:00 PM'
ENCOUNTER_DURATION_MINUTES = 45
ENCOUNTER_END_TIME = DateValues.add_minutes_to_time(
   ENCOUNTER_START_TIME,
   ENCOUNTER_DURATION_MINUTES )


@pytest.fixture
def unschedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULE_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, ?, ?, 1 );
      """,
      ( LION_SPECIES, LION_EXHIBIT, LION_START_TIME, LION_END_TIME ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( CAROUSEL, CAROUSEL_START_TIME, CAROUSEL_END_TIME ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, LUNCH_START_TIME, LUNCH_END_TIME ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def zoomobile_unschedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULE_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 1, ?, ?, ?, 1 );
      """,
      (
         TransportationName.ZOOMOBILE,
         ZOOMOBILE_START_TIME,
         ZOOMOBILE_END_TIME,
         'summer',
      ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 1, ?, ?, ?, ? );
      """,
      (
         TransportationName.ZOOMOBILE,
         MAIN,
         CANADA,
         ZOOMOBILE_START_TIME,
         DateValues.add_minutes_to_time(
            ZOOMOBILE_START_TIME,
            LEG_DURATION_MINUTES ),
      ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationRouteMarker (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               SEQUENCE,
               MARKER_ORDER,
               MARKER_ID
            )
            VALUES ( ?, 1, ?, ?, ? );
      """,
      (
         TransportationName.ZOOMOBILE,
         Position.FIRST,
         Position.FIRST,
         'm-a',
      ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def guardians_unschedule_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.executescript( UNSCHEDULE_SCHEMA + GUARDIANS_SCHEMA )
   conn.execute(
      'INSERT INTO ItineraryGuardiansTalk ( TALK_NAME, START_TIME, END_TIME ) VALUES ( ?, ?, ? );',
      ( LION_TALK, TALK_START_TIME, TALK_END_TIME ) )
   conn.execute(
      'INSERT INTO ItineraryWildEncounter ( WILD_ENCOUNTER, START_TIME, END_TIME ) VALUES ( ?, ?, ? );',
      ( RHINO_ENCOUNTER, ENCOUNTER_START_TIME, ENCOUNTER_END_TIME ) )
   conn.commit()
   yield conn
   conn.close()


def Test_ClearItineraryAnimalSchedule_TestScheduledAnimal_ExpectClearedTimes(
      unschedule_conn: sqlite3.Connection ) -> None:
   species = LION_SPECIES
   exhibit = LION_EXHIBIT
   cur = unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
      cur,
      species=species,
      exhibit=exhibit )
   unschedule_conn.commit()
   cur.close()
   row = unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME, COVERED_BY_TALK
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( species, exhibit ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None
   assert row[ 'COVERED_BY_TALK' ] == 0


def Test_ClearItineraryAttractionSchedule_TestScheduledAttraction_ExpectClearedTimes(
      unschedule_conn: sqlite3.Connection ) -> None:
   name = CAROUSEL
   cur = unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.clear_itinerary_attraction_schedule(
      cur,
      name=name )
   unschedule_conn.commit()
   cur.close()
   row = unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( name, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_DeleteItineraryEventSchedule_TestScheduledEvent_ExpectRowDeleted(
      unschedule_conn: sqlite3.Connection ) -> None:
   event_type = ItineraryEventType.LUNCH
   cur = unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.delete_itinerary_event_schedule(
      cur,
      event_type=event_type )
   unschedule_conn.commit()
   cur.close()
   row = unschedule_conn.execute(
      """   SELECT EVENT_TYPE
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( event_type.value, ),
   ).fetchone()

   assert row is None


def Test_ClearItineraryTransportationSchedule_TestScheduledZoomobile_ExpectClearedTimesLegsAndMarkers(
      zoomobile_unschedule_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   cur = zoomobile_unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
      cur,
      name=transportation,
      added_as_attraction=added_as_attraction )
   zoomobile_unschedule_conn.commit()
   cur.close()
   transportation_row = zoomobile_unschedule_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( transportation, ),
   ).fetchone()
   leg_count = zoomobile_unschedule_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( transportation, ),
   ).fetchone()
   marker_count = zoomobile_unschedule_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryTransportationRouteMarker
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( transportation, ),
   ).fetchone()

   assert transportation_row is not None
   assert transportation_row[ 'START_TIME' ] is None
   assert transportation_row[ 'END_TIME' ] is None
   assert transportation_row[ 'ROUTE' ] is None
   assert transportation_row[ 'BULK_TRANSIT_EVALUATED' ] == 0
   assert leg_count is not None
   assert leg_count[ 'COUNT' ] == 0
   assert marker_count is not None
   assert marker_count[ 'COUNT' ] == 0


def Test_ClearItineraryGuardiansTalkSchedule_TestTalk_ExpectDeleted(
      guardians_unschedule_conn: sqlite3.Connection ) -> None:
   talk_name = LION_TALK
   cur = guardians_unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.clear_itinerary_guardians_talk_schedule(
      cur,
      talk_name=talk_name )
   guardians_unschedule_conn.commit()
   remaining_count = guardians_unschedule_conn.execute(
      'SELECT COUNT(*) FROM ItineraryGuardiansTalk' ).fetchone()[ Position.FIRST ]

   assert remaining_count == 0


def Test_ClearItineraryWildEncounterSchedule_TestEncounter_ExpectDeleted(
      guardians_unschedule_conn: sqlite3.Connection ) -> None:
   wild_encounter = RHINO_ENCOUNTER
   cur = guardians_unschedule_conn.cursor()

   UnscheduleItineraryItemProvider.clear_itinerary_wild_encounter_schedule(
      cur,
      wild_encounter=wild_encounter )
   guardians_unschedule_conn.commit()
   remaining_count = guardians_unschedule_conn.execute(
      'SELECT COUNT(*) FROM ItineraryWildEncounter' ).fetchone()[ Position.FIRST ]

   assert remaining_count == 0
