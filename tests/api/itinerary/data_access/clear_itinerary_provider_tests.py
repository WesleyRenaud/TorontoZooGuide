from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.clear_itinerary_provider import ClearItineraryProvider
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.shared.enums import ItineraryErrorType


CLEAR_ITINERARY_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

CREATE TABLE ItineraryExhibit (
   EXHIBIT              TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   ENCLOSURE_NAME       TEXT,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   FROM_STATION             TEXT NOT NULL,
   TO_STATION               TEXT NOT NULL,
   START_TIME               TEXT NOT NULL,
   END_TIME                 TEXT NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER NOT NULL,
   MARKER_ORDER             INTEGER NOT NULL,
   MARKER_ID                TEXT NOT NULL
);

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryWalkRouteStop (
   STOP_SEQUENCE          INTEGER NOT NULL PRIMARY KEY,
   SCHEDULE_ITEM_KIND     TEXT NOT NULL,
   ITEM_KEY               TEXT NOT NULL,
   WALK_NODE_ID           TEXT NOT NULL
);

CREATE TABLE ItineraryWalkRoutePoint (
   POINT_SEQUENCE         INTEGER NOT NULL PRIMARY KEY,
   WALK_NODE_ID           TEXT NOT NULL,
   X                      REAL NOT NULL,
   Y                      REAL NOT NULL,
   X_PX                   REAL NOT NULL,
   Y_PX                   REAL NOT NULL
);

CREATE TABLE ItineraryWalkRouteLeg (
   LEG_SEQUENCE               INTEGER NOT NULL PRIMARY KEY,
   FROM_ITEM_KEY              TEXT NOT NULL,
   TO_ITEM_KEY                TEXT NOT NULL,
   FROM_SCHEDULE_ITEM_KIND    TEXT NOT NULL,
   TO_SCHEDULE_ITEM_KIND      TEXT NOT NULL,
   FROM_POINT_SEQUENCE        INTEGER NOT NULL,
   TO_POINT_SEQUENCE          INTEGER NOT NULL,
   TRAVEL_TIME_MINUTES        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryStatus (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSABLE    BOOL NOT NULL
);

CREATE TABLE ItineraryStatusSuppression (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSED      BOOL NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def clear_itinerary_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( CLEAR_ITINERARY_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( '2026-06-15', '9:30 AM', '5:00 PM' ) )
   conn.execute(
      'INSERT INTO ItineraryAnimal ( SPECIES, EXHIBIT ) VALUES ( ?, ? );',
      ( 'African Lion', 'Africa Savanna' ) )
   conn.execute(
      """   INSERT INTO ItineraryStatus (
               STATUS,
               IS_SUPPRESSABLE
            )
            VALUES ( ?, 1 );
      """,
      ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_ClearItinerary_TestSavedRows_ExpectTablesCleared(
      clear_itinerary_conn: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      clear_itinerary_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert ClearItineraryProvider.clear_itinerary( clear_itinerary_conn )

   date_count = clear_itinerary_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryDate;' ).fetchone()
   animal_count = clear_itinerary_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;' ).fetchone()

   assert date_count is not None
   assert date_count[ 'COUNT' ] == 0
   assert animal_count is not None
   assert animal_count[ 'COUNT' ] == 0
   assert ItineraryStatusProvider.is_itinerary_error_suppressed(
      clear_itinerary_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def Test_ClearItinerary_TestSavedRows_ExpectProviderReadsEmpty(
      clear_itinerary_conn: sqlite3.Connection ) -> None:
   assert ClearItineraryProvider.clear_itinerary( clear_itinerary_conn )

   assert ItineraryProvider.fetch_itinerary_date( clear_itinerary_conn ) is None

   cleared = ItineraryProvider.fetch_saved_itinerary( clear_itinerary_conn )

   assert cleared.is_empty()
   assert cleared.animal_rows == []
   assert cleared.attraction_rows == []
   assert cleared.guardians_talk_rows == []
   assert cleared.wild_encounter_rows == []
