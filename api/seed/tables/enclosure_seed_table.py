from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'species',
   'exhibit',
   'seasonal_viewing_summary',
   'seasonal_viewing_information',
   'include_all_viewing_spots',
]

DB_COLUMNS = [
   'SPECIES',
   'EXHIBIT',
   'SEASONAL_VIEWING_SUMMARY',
   'SEASONAL_VIEWING_INFORMATION',
   'INCLUDE_ALL_VIEWING_SPOTS',
]

DATA_FILE = 'enclosure.json'

SQL_FILE = 'enclosure.sql'


class EnclosureSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='Enclosure',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


enclosures = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
