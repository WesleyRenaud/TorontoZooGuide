from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'x_coord',
   'y_coord',
]

DB_COLUMNS = [
   'X_COORD',
   'Y_COORD',
]

DATA_FILE = 'defibrillator.json'

SQL_FILE = 'defibrillator.sql'


class DefibrillatorSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='Defibrillator',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


defibrillators = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
