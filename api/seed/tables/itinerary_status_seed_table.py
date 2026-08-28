from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'status',
   'is_suppressable',
]

DB_COLUMNS = [
   'STATUS',
   'IS_SUPPRESSABLE',
]

DATA_FILE = 'itinerary_status.json'

SQL_FILE = 'itinerary_status.sql'


class ItineraryStatusSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='ItineraryStatus',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


itinerary_statuses = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
