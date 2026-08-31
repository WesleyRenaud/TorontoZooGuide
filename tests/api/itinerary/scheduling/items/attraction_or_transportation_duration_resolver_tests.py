from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.scheduling.items.attraction_or_transportation_duration_resolver import AttractionOrTransportationDurationResolver


DURATION_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL,
   IS_ALSO_TRANSPORTATION               INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'


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
      ( CAROUSEL, 12 ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, NULL, 1 );
      """,
      ( ZOOMOBILE, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_DefaultSeconds_TestAttraction_ExpectAttractionDuration(
      duration_conn: sqlite3.Connection ) -> None:
   assert AttractionOrTransportationDurationResolver.default_seconds(
      duration_conn,
      CAROUSEL ) == 12 * 60


def Test_DefaultSeconds_TestTransportationAttraction_ExpectTransportationDuration(
      duration_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_or_transportation_duration_resolver.TransportationDefaultDurationResolver.resolve',
      lambda conn, attraction_name: 25 * 60 )

   assert AttractionOrTransportationDurationResolver.default_seconds(
      duration_conn,
      ZOOMOBILE ) == 25 * 60
