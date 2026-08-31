from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_event_default_provider import ItineraryEventDefaultProvider
from api.shared.enums import ItineraryEventType


EVENT_DEFAULT_SCHEMA = """
CREATE TABLE ItineraryEventDefault (
   EVENT_TYPE                            TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES    INTEGER     NOT NULL
);
"""

OWNED_EVENT_DEFAULTS = [
   ( ItineraryEventType.BREAKFAST.value, 30 ),
   ( ItineraryEventType.LUNCH.value, 40 ),
   ( ItineraryEventType.DINNER.value, 45 ),
   ( ItineraryEventType.SNACK.value, 15 ),
   ( ItineraryEventType.BREAK.value, 20 ),
   ( ItineraryEventType.SHOPPING.value, 30 ),
]


@pytest.fixture
def event_default_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EVENT_DEFAULT_SCHEMA )
   conn.executemany(
      """   INSERT INTO ItineraryEventDefault (
               EVENT_TYPE,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ? );
      """,
      OWNED_EVENT_DEFAULTS )

   yield conn

   conn.close()


def Test_FetchRecords_TestOwnedRows_ExpectMappedEventDefaults(
      event_default_conn: sqlite3.Connection ) -> None:
   records = ItineraryEventDefaultProvider.fetch_records( event_default_conn )

   assert len( records ) == len( OWNED_EVENT_DEFAULTS )
   assert {
      record.event_type for record in records
   } == {
      ItineraryEventType.BREAKFAST,
      ItineraryEventType.LUNCH,
      ItineraryEventType.DINNER,
      ItineraryEventType.SNACK,
      ItineraryEventType.BREAK,
      ItineraryEventType.SHOPPING,
   }

   lunch = next(
      record for record in records
      if record.event_type == ItineraryEventType.LUNCH
   )

   assert lunch.default_duration_minutes == 40
