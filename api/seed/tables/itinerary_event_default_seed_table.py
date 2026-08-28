from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'event_type',
   'default_itinerary_duration_minutes',
]

DB_COLUMNS = [
   'EVENT_TYPE',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
]

DATA_FILE = 'itinerary_event_default.json'

SQL_FILE = 'itinerary_event_default.sql'


class ItineraryEventDefaultSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='ItineraryEventDefault',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


itinerary_event_defaults = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
