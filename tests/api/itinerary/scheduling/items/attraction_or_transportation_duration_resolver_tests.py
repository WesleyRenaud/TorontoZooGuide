from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.scheduling.items.attraction_or_transportation_duration_resolver import AttractionOrTransportationDurationResolver
from api.shared.duration_values import DurationValues
from api.shared.enums.transportation_name import TransportationName


DURATION_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL,
   IS_ALSO_TRANSPORTATION               INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
CAROUSEL_DURATION_MINUTES = 12


@pytest.fixture
def duration_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( DURATION_SCHEMA )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, ?, 0 );
      """,
      ( CAROUSEL, CAROUSEL_DURATION_MINUTES ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, NULL, 1 );
      """,
      ( TransportationName.ZOOMOBILE, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_DefaultSeconds_TestAttraction_ExpectAttractionDuration(
      duration_conn: sqlite3.Connection ) -> None:
   seconds = AttractionOrTransportationDurationResolver.default_seconds(
      duration_conn,
      CAROUSEL )

   assert seconds == DurationValues.minutes_to_seconds( CAROUSEL_DURATION_MINUTES )


def Test_DefaultSeconds_TestTransportationAttraction_ExpectTransportationDuration(
      duration_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportation_minutes = 25
   transportation_seconds = DurationValues.minutes_to_seconds(
      transportation_minutes )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_or_transportation_duration_resolver.TransportationDefaultDurationResolver.resolve',
      lambda conn, attraction_name: transportation_seconds )

   seconds = AttractionOrTransportationDurationResolver.default_seconds(
      duration_conn,
      TransportationName.ZOOMOBILE )

   assert seconds == transportation_seconds
