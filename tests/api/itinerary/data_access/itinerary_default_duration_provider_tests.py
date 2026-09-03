from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
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
      ( 'African Lion', 'Africa Savanna', 0.5 ) )
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
      ( 'African Lion', 'Africa Savanna', 'Outdoor' ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ? );
      """,
      ( 'Splash Island', 15 ) )
   conn.execute(
      """   INSERT INTO ItineraryEventDefault (
               EVENT_TYPE,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, 30 ) )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestHalfMinute_ExpectThirtySeconds(
      default_duration_conn: sqlite3.Connection ) -> None:
   duration = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      default_duration_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name=None )

   assert duration == 30


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestNamedEnclosureMissing_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      extended_default_duration_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Missing Enclosure' ) is None


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestNamedEnclosureNullMinutes_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      extended_default_duration_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' ) is None


def Test_FetchAttractionDefaultDurationSeconds_TestMissingAttraction_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds(
      extended_default_duration_conn,
      'Unknown Ride' ) is None


def Test_FetchAttractionDefaultDurationSeconds_TestPresent_ExpectSeconds(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds(
      extended_default_duration_conn,
      'Splash Island' ) == 15 * 60


def Test_FetchEventDefaultDurationSeconds_TestLunchPresent_ExpectSeconds(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds(
      extended_default_duration_conn,
      ItineraryEventType.LUNCH ) == 30 * 60


def Test_FetchEventDefaultDurationSeconds_TestMissingEvent_ExpectNone(
      extended_default_duration_conn: sqlite3.Connection ) -> None:
   assert ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds(
      extended_default_duration_conn,
      ItineraryEventType.ARRIVAL ) is None
