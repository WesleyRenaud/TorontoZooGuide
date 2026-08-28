from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'transportation',
   'name',
   'description',
   'x_coord',
   'y_coord',
   'is_main_station',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'NAME',
   'DESCRIPTION',
   'X_COORD',
   'Y_COORD',
   'IS_MAIN_STATION',
]

DATA_FILE = 'transportation_station.json'

SQL_FILE = 'transportation_station.sql'


class TransportationStationSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='TransportationStation',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


transportation_stations = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
