from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_provider import ItineraryProvider


ITINERARY_PROVIDER_SCHEMA = """
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
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER NOT NULL DEFAULT 0,
   COVERED_BY_TALK       INTEGER NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER NOT NULL DEFAULT 0
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
"""


@pytest.fixture
def itinerary_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ITINERARY_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchItineraryDate_TestEmptyDatabase_ExpectNone(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   assert ItineraryProvider.fetch_itinerary_date( itinerary_provider_conn ) is None


def Test_FetchItineraryDate_TestSavedDate_ExpectVisitDate(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( '2026-06-15', '9:30 AM', '5:00 PM' ) )
   itinerary_provider_conn.commit()

   assert ItineraryProvider.fetch_itinerary_date(
      itinerary_provider_conn ) == '2026-06-15'


def Test_FetchSavedItinerary_TestEmptyDatabase_ExpectEmpty(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   saved = ItineraryProvider.fetch_saved_itinerary( itinerary_provider_conn )

   assert saved.is_empty()
   assert saved.animal_rows == []
   assert saved.guardians_talk_rows == []
   assert saved.wild_encounter_rows == []


def Test_FetchSavedItinerary_TestSavedRows_ExpectPersistedContent(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( '2026-06-15', '9:30 AM', '5:00 PM' ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', None, 100 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'Conservation Carousel', None, 100 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( 'African Lion', '10:00 AM', '10:30 AM', 0 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( 'African Rainforest', '2:00 PM', '2:45 PM', 0 ) )
   itinerary_provider_conn.commit()

   saved = ItineraryProvider.fetch_saved_itinerary( itinerary_provider_conn )

   assert saved.date_value == '2026-06-15'
   assert saved.arrival_time == '9:30 AM'
   assert saved.departure_time == '5:00 PM'
   assert saved.animal_rows[ 0 ].species == 'African Lion'
   assert saved.attraction_rows[ 0 ].attraction == 'Conservation Carousel'
   assert saved.guardians_talk_rows[ 0 ].talk_name == 'African Lion'
   assert saved.guardians_talk_rows[ 0 ].start_time == '10:00 AM'
   assert saved.wild_encounter_rows[ 0 ].wild_encounter == 'African Rainforest'
   assert saved.wild_encounter_rows[ 0 ].start_time == '2:00 PM'
