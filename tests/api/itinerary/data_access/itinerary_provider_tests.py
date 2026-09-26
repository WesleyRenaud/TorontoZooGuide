from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


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
   SPECIES                 TEXT NOT NULL,
   EXHIBIT                 TEXT NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT
);

CREATE TABLE TransportationAnimal (
   TRANSPORTATION      TEXT NOT NULL,
   FROM_STATION        TEXT NOT NULL,
   TO_STATION          TEXT NOT NULL,
   SPECIES             TEXT NOT NULL,
   EXHIBIT             TEXT NOT NULL,
   ENCLOSURE_NAME      TEXT
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
   itinerary_date = ItineraryProvider.fetch_itinerary_date(
      itinerary_provider_conn )

   assert itinerary_date is None


def Test_FetchItineraryDate_TestSavedDate_ExpectVisitDate(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   visit_date = '2026-06-15'
   arrival_time = '9:30 AM'
   departure_time = '5:00 PM'
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( visit_date, arrival_time, departure_time ) )
   itinerary_provider_conn.commit()

   itinerary_date = ItineraryProvider.fetch_itinerary_date(
      itinerary_provider_conn )

   assert itinerary_date == visit_date


def Test_FetchSavedItinerary_TestEmptyDatabase_ExpectEmpty(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   saved = ItineraryProvider.fetch_saved_itinerary( itinerary_provider_conn )

   assert saved.is_empty()
   assert saved.animal_rows == []
   assert saved.guardians_talk_rows == []
   assert saved.wild_encounter_rows == []


def Test_FetchSavedItinerary_TestSavedRows_ExpectPersistedContent(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   visit_date = '2026-06-15'
   arrival_time = '9:30 AM'
   departure_time = '5:00 PM'
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   attraction = 'Conservation Carousel'
   talk_name = 'African Lion'
   talk_start_time = '10:00 AM'
   talk_duration_minutes = 30
   talk_end_time = DateValues.add_minutes_to_time(
      talk_start_time,
      talk_duration_minutes )
   encounter_name = 'African Rainforest'
   encounter_start_time = '2:00 PM'
   encounter_duration_minutes = 45
   encounter_end_time = DateValues.add_minutes_to_time(
      encounter_start_time,
      encounter_duration_minutes )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( visit_date, arrival_time, departure_time ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( species, exhibit, None, 100 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ? );
      """,
      ( attraction, None, 100 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( talk_name, talk_start_time, talk_end_time, 0 ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( encounter_name, encounter_start_time, encounter_end_time, 0 ) )
   itinerary_provider_conn.commit()

   saved = ItineraryProvider.fetch_saved_itinerary( itinerary_provider_conn )

   assert saved.date_value == visit_date
   assert saved.arrival_time == arrival_time
   assert saved.departure_time == departure_time
   assert saved.animal_rows[ Position.FIRST ].species == species
   assert saved.animal_rows[ Position.FIRST ].transportation is None
   assert saved.attraction_rows[ Position.FIRST ].attraction == attraction
   assert saved.guardians_talk_rows[ Position.FIRST ].talk_name == talk_name
   assert saved.guardians_talk_rows[ Position.FIRST ].start_time == talk_start_time
   assert saved.wild_encounter_rows[ Position.FIRST ].wild_encounter == encounter_name
   assert saved.wild_encounter_rows[ Position.FIRST ].start_time == encounter_start_time


def Test_FetchItineraryAnimalRows_TestAddedByTransportation_ExpectCatalogTransportation(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   from_station = 'Canadian Domain Zoomobile Station'
   to_station = 'Africa Zoomobile Station'
   species = 'Masai Giraffe'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   itinerary_provider_conn.execute(
      """   INSERT INTO TransportationAnimal (
               TRANSPORTATION,
               FROM_STATION,
               TO_STATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      (
         transportation,
         from_station,
         to_station,
         species,
         exhibit,
         enclosure_name,
      ) )
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               ADDED_BY_TRANSPORTATION
            )
            VALUES ( ?, ?, ?, 1 );
      """,
      ( species, exhibit, enclosure_name ) )
   itinerary_provider_conn.commit()

   giraffe = ItineraryProvider.fetch_itinerary_animal_rows(
      itinerary_provider_conn )[ Position.FIRST ]

   assert giraffe.added_by_transportation is True
   assert giraffe.transportation == transportation


def Test_FetchItineraryTransportationLegRows_TestSavedLegs_ExpectMappedLegs(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   main_station = 'Main Zoomobile Station'
   canada_station = 'Canadian Domain Zoomobile Station'
   africa_station = 'Africa Zoomobile Station'
   start_time = '10:00 AM'
   first_duration_minutes = 20
   first_end_time = DateValues.add_minutes_to_time(
      start_time,
      first_duration_minutes )
   second_duration_minutes = 10
   second_end_time = DateValues.add_minutes_to_time(
      first_end_time,
      second_duration_minutes )
   itinerary_provider_conn.execute(
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
         transportation,
         main_station,
         canada_station,
         start_time,
         first_end_time,
      ) )
   itinerary_provider_conn.execute(
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
         transportation,
         canada_station,
         africa_station,
         first_end_time,
         second_end_time,
      ) )
   itinerary_provider_conn.commit()

   legs = ItineraryProvider.fetch_itinerary_transportation_leg_rows(
      itinerary_provider_conn )

   assert len( legs ) == 2
   assert all( isinstance( leg, ItineraryTransportationLeg ) for leg in legs )
   assert legs[ Position.FIRST ].transportation == transportation
   assert legs[ Position.FIRST ].from_station == main_station
   assert legs[ Position.LAST ].to_station == africa_station


def Test_FetchItineraryTransportationNames_TestSavedRows_ExpectTransportationNames(
      itinerary_provider_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = 0
   itinerary_provider_conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION
            )
            VALUES ( ?, ? );
      """,
      ( transportation, added_as_attraction ) )
   itinerary_provider_conn.commit()

   names = ItineraryProvider.fetch_itinerary_transportation_names(
      itinerary_provider_conn )

   assert names == { transportation }
