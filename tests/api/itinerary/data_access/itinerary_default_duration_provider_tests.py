from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from api.shared.duration_values import DurationValues
from api.shared.enums import ItineraryEventType


DEFAULT_DURATION_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES                          TEXT        NOT NULL,
   EXHIBIT                          TEXT        NOT NULL,
   NAME                             TEXT,
   DEFAULT_ITINERARY_DURATION_MINUTES REAL
);
"""

EXTENDED_DEFAULT_DURATION_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL
);

CREATE TABLE ItineraryEventDefault (
   EVENT_TYPE                           TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL
);
"""

LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
LION_ENCLOSURE = 'Outdoor'
LION_DURATION_MINUTES = 0.5
SPLASH_ISLAND = 'Splash Island'
SPLASH_ISLAND_DURATION_MINUTES = 15
LUNCH_DURATION_MINUTES = 30


@pytest.fixture
def default_duration_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DEFAULT_DURATION_SCHEMA )
   conn.execute(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ?, NULL, ? );
      """,
      ( LION_SPECIES, LION_EXHIBIT, LION_DURATION_MINUTES ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def extended_default_duration_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DEFAULT_DURATION_SCHEMA )
   conn.executescript( EXTENDED_DEFAULT_DURATION_SCHEMA )
   conn.execute(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ?, ?, NULL );
      """,
      ( LION_SPECIES, LION_EXHIBIT, LION_ENCLOSURE ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ? );
      """,
      ( SPLASH_ISLAND, SPLASH_ISLAND_DURATION_MINUTES ) )
   conn.execute(
      """   INSERT INTO ItineraryEventDefault (
               EVENT_TYPE,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, LUNCH_DURATION_MINUTES ) )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestHalfMinute_ExpectThirtySeconds(
      default_duration_conn: sqlite3.Connection ) -> None:
   duration = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      default_duration_conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      enclosure_name=None )

   assert duration == DurationValues.normalize_seconds( LION_DURATION_MINUTES )


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestNamedEnclosureMissing_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   enclosure_name = 'Missing Enclosure'

   duration = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      extended_default_duration_conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      enclosure_name=enclosure_name )

   assert duration is None


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestNamedEnclosureNullMinutes_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   duration = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      extended_default_duration_conn,
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      enclosure_name=LION_ENCLOSURE )

   assert duration is None


def Test_FetchAttractionDefaultDurationSeconds_TestMissingAttraction_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   attraction = 'Unknown Ride'

   duration = ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds(
      extended_default_duration_conn,
      attraction )

   assert duration is None


def Test_FetchAttractionDefaultDurationSeconds_TestPresent_ExpectSeconds(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   duration = ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds(
      extended_default_duration_conn,
      SPLASH_ISLAND )

   assert duration == DurationValues.normalize_seconds(
      SPLASH_ISLAND_DURATION_MINUTES )


def Test_FetchEventDefaultDurationSeconds_TestLunchPresent_ExpectSeconds(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   event_type = ItineraryEventType.LUNCH

   duration = ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds(
      extended_default_duration_conn,
      event_type )

   assert duration == DurationValues.normalize_seconds( LUNCH_DURATION_MINUTES )


def Test_FetchEventDefaultDurationSeconds_TestMissingEvent_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   event_type = ItineraryEventType.ARRIVAL

   duration = ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds(
      extended_default_duration_conn,
      event_type )

   assert duration is None
