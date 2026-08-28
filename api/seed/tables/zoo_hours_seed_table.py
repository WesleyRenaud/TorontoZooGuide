from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'operating_date',
   'early_admission_time',
   'open_time',
   'last_admission_time',
   'close_time',
]

DB_COLUMNS = [
   'OPERATING_DATE',
   'EARLY_ADMISSION_TIME',
   'OPEN_TIME',
   'LAST_ADMISSION_TIME',
   'CLOSE_TIME',
]

DATA_FILE = 'zoo_hours.json'

SQL_FILE = 'zoo_hours.sql'


class ZooHoursSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='ZooHours',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


zoo_hours = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
