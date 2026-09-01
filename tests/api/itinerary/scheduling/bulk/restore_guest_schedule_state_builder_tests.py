from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.scheduling.bulk.restore_guest_schedule_state_builder import RestoreGuestScheduleStateBuilder
from api.shared.enums import ItineraryEventType


RESTORE_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

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

CREATE TABLE ItineraryWalkRouteStop (
   STOP_SEQUENCE            INTEGER     NOT NULL,
   SCHEDULE_ITEM_KIND       TEXT,
   ITEM_KEY                 TEXT,
   WALK_NODE_ID             TEXT,
   START_TIME               TEXT,
   END_TIME                 TEXT
);

CREATE TABLE ItineraryWalkRoutePoint (
   POINT_SEQUENCE           INTEGER     NOT NULL,
   WALK_NODE_ID             TEXT,
   X                        REAL,
   Y                        REAL,
   X_PX                     REAL,
   Y_PX                     REAL
);

CREATE TABLE ItineraryWalkRouteLeg (
   LEG_SEQUENCE             INTEGER     NOT NULL,
   FROM_ITEM_KEY            TEXT,
   TO_ITEM_KEY              TEXT,
   FROM_SCHEDULE_ITEM_KIND  TEXT,
   TO_SCHEDULE_ITEM_KIND    TEXT,
   FROM_POINT_SEQUENCE      INTEGER,
   TO_POINT_SEQUENCE        INTEGER,
   TRAVEL_TIME_MINUTES      INTEGER
);

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

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:00 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species=LION_SPECIES,
         exhibit=LION_EXHIBIT,
         old_likelihood=None,
         new_likelihood=100,
         start_time='10:00 AM',
         end_time='10:08 AM',
      ),
      ItineraryAnimalRecord(
         species='Cheetah',
         exhibit=LION_EXHIBIT,
         old_likelihood=None,
         new_likelihood=100,
         start_time=None,
         end_time=None,
      ),
   ],
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction=CAROUSEL,
         old_likelihood=None,
         new_likelihood=100,
         start_time='11:00 AM',
         end_time='11:20 AM',
      ),
   ],
   event_rows=[
      ItineraryEventRecord(
         event_type=ItineraryEventType.LUNCH,
         start_time='12:00 PM',
         end_time='12:40 PM',
      ),
   ],
)

EMPTY_WALK_ROUTE = ItineraryWalkRoute( stops=[], legs=[], points=[] )


@pytest.fixture
def restore_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTORE_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( '2026-06-15', '8:00 AM', '6:00 PM' );
      """ )
   conn.executemany(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, 0 );
      """,
      [
         ( LION_SPECIES, LION_EXHIBIT ),
         ( 'Cheetah', LION_EXHIBIT ),
      ] )
   conn.execute(
      'INSERT INTO ItineraryAttraction ( ATTRACTION ) VALUES ( ? );',
      ( CAROUSEL, ) )
   conn.execute(
      'INSERT INTO ItineraryEvent ( EVENT_TYPE ) VALUES ( ? );',
      ( ItineraryEventType.LUNCH.value, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Snapshot_TestSavedItinerary_ExpectSameItineraryAndWalkRoute(
      restore_conn: sqlite3.Connection ) -> None:
   saved_itinerary, walk_route = RestoreGuestScheduleStateBuilder.snapshot(
      restore_conn,
      SAVED_ITINERARY )

   assert saved_itinerary is SAVED_ITINERARY
   assert walk_route.stops == []
   assert walk_route.legs == []
   assert walk_route.points == []


def Test_Restore_TestSnapshotState_ExpectScheduledRowsAndTimesRestored(
      restore_conn: sqlite3.Connection ) -> None:
   RestoreGuestScheduleStateBuilder.restore(
      restore_conn,
      SAVED_ITINERARY,
      EMPTY_WALK_ROUTE )

   lion = restore_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION_SPECIES, ),
   ).fetchone()
   cheetah = restore_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( 'Cheetah', ),
   ).fetchone()
   carousel = restore_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()
   lunch = restore_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
      """,
      ( ItineraryEventType.LUNCH.value, ),
   ).fetchone()
   times = restore_conn.execute(
      'SELECT ARRIVAL_TIME, DEPARTURE_TIME FROM ItineraryDate;' ).fetchone()

   assert lion is not None
   assert lion[ 'START_TIME' ] == '10:00 AM'
   assert lion[ 'END_TIME' ] == '10:08 AM'
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] is None
   assert cheetah[ 'END_TIME' ] is None
   assert carousel is not None
   assert carousel[ 'START_TIME' ] == '11:00 AM'
   assert lunch is not None
   assert lunch[ 'START_TIME' ] == '12:00 PM'
   assert times is not None
   assert times[ 'ARRIVAL_TIME' ] == '9:00 AM'
   assert times[ 'DEPARTURE_TIME' ] == '5:00 PM'
