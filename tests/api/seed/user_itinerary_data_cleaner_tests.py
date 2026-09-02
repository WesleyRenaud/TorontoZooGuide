from __future__ import annotations

from pathlib import Path
import sqlite3

import pytest

from api.seed.user_itinerary_data_cleaner import UserItineraryDataCleaner


ITINERARY_CLEANER_SCHEMA = """
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
   STOP_SEQUENCE            INTEGER NOT NULL PRIMARY KEY,
   SCHEDULE_ITEM_KIND       TEXT,
   ITEM_KEY                 TEXT,
   WALK_NODE_ID             TEXT,
   START_TIME               TEXT,
   END_TIME                 TEXT
);

CREATE TABLE ItineraryWalkRoutePoint (
   POINT_SEQUENCE           INTEGER NOT NULL PRIMARY KEY,
   WALK_NODE_ID             TEXT,
   X                        REAL,
   Y                        REAL,
   X_PX                     REAL,
   Y_PX                     REAL
);

CREATE TABLE ItineraryWalkRouteLeg (
   LEG_SEQUENCE             INTEGER NOT NULL PRIMARY KEY,
   FROM_ITEM_KEY            TEXT,
   TO_ITEM_KEY              TEXT,
   FROM_SCHEDULE_ITEM_KIND  TEXT,
   TO_SCHEDULE_ITEM_KIND    TEXT,
   FROM_POINT_SEQUENCE      INTEGER,
   TO_POINT_SEQUENCE        INTEGER,
   TRAVEL_TIME_MINUTES      INTEGER
);
"""


@pytest.fixture
def itinerary_cleaner_conn( tmp_path: Path ) -> sqlite3.Connection:
   path = tmp_path / 'animals.db'
   conn = sqlite3.connect( path )
   conn.executescript( ITINERARY_CLEANER_SCHEMA )
   conn.executescript(
      """
      INSERT INTO ItineraryDate ( ITINERARY_DATE, ARRIVAL_TIME, DEPARTURE_TIME )
      VALUES ( '2026-06-15', '09:30', '16:00' );
      INSERT INTO ItineraryExhibit ( EXHIBIT ) VALUES ( 'Africa Savanna' );
      INSERT INTO ItineraryAnimal ( SPECIES, EXHIBIT )
      VALUES ( 'African Lion', 'Africa Savanna' );
      INSERT INTO ItineraryAttraction ( ATTRACTION )
      VALUES ( 'Conservation Carousel' );
      INSERT INTO ItineraryGuardiansTalk ( TALK_NAME )
      VALUES ( 'African Lion' );
      INSERT INTO ItineraryWildEncounter ( WILD_ENCOUNTER )
      VALUES ( 'African Rainforest' );
      INSERT INTO ItineraryEvent ( EVENT_TYPE )
      VALUES ( 'lunch' );
      INSERT INTO ItineraryWalkRouteStop ( STOP_SEQUENCE, ITEM_KEY )
      VALUES ( 1, 'African Lion' );
      INSERT INTO ItineraryWalkRoutePoint ( POINT_SEQUENCE, X, Y )
      VALUES ( 1, 1.0, 2.0 );
      INSERT INTO ItineraryWalkRouteLeg ( LEG_SEQUENCE, FROM_ITEM_KEY, TO_ITEM_KEY )
      VALUES ( 1, 'A', 'B' );
      """ )
   conn.commit()

   yield conn

   conn.close()


def Test_Clear_TestPopulatedItinerary_ExpectClearsAllTables(
      itinerary_cleaner_conn: sqlite3.Connection ) -> None:
   cur = itinerary_cleaner_conn.cursor()
   UserItineraryDataCleaner.clear( cur )
   itinerary_cleaner_conn.commit()
   cur.close()

   tables = [
      'ItineraryDate',
      'ItineraryExhibit',
      'ItineraryAnimal',
      'ItineraryAttraction',
      'ItineraryGuardiansTalk',
      'ItineraryWildEncounter',
      'ItineraryEvent',
      'ItineraryWalkRouteStop',
      'ItineraryWalkRoutePoint',
      'ItineraryWalkRouteLeg',
   ]

   for table in tables:
      count = itinerary_cleaner_conn.execute(
         f'SELECT COUNT(*) FROM { table };' ).fetchone()[ 0 ]
      assert count == 0


def Test_Main_TestDatabasePath_ExpectClearsAndPrintsSuccess(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   path = tmp_path / 'animals.db'
   conn = sqlite3.connect( path )
   conn.executescript( ITINERARY_CLEANER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryExhibit ( EXHIBIT )
            VALUES ( 'Africa Savanna' );
      """ )
   conn.commit()
   conn.close()

   UserItineraryDataCleaner.main( str( path ) )

   conn = sqlite3.connect( path )
   count = conn.execute( 'SELECT COUNT(*) FROM ItineraryExhibit;' ).fetchone()[ 0 ]
   conn.close()

   assert count == 0
   assert 'User itinerary data cleared successfully.' in capsys.readouterr().out
