from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider


DEFAULT_DURATION_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES                          TEXT        NOT NULL,
   EXHIBIT                          TEXT        NOT NULL,
   NAME                             TEXT,
   DEFAULT_ITINERARY_DURATION_MINUTES REAL
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


def Test_FetchEnclosureViewingDefaultDurationSeconds_TestHalfMinute_ExpectThirtySeconds(
      default_duration_conn: sqlite3.Connection ) -> None:
   duration = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
      default_duration_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name=None )

   assert duration == 30
