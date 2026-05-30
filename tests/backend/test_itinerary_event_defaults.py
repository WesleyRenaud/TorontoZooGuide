from __future__ import annotations

import sqlite3

from api.itinerary.data_access.itinerary_event_default import fetch_itinerary_event_default_records
from api.seed.tables import itinerary_event_default
from api.shared.enums import ItineraryEventType


def connect_test_database() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   return conn


def test_itinerary_event_defaults_are_seeded() -> None:
   conn = connect_test_database()
   cursor = conn.cursor()

   itinerary_event_default.create_table( cursor )
   itinerary_event_default.insert_rows( cursor )

   records = fetch_itinerary_event_default_records( conn )

   assert len( records ) == len( itinerary_event_default.itinerary_event_defaults )
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
