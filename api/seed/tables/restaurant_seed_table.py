from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'name',
   'location',
   'sub_location',
   'description',
   'menu_link',
   'x_coord',
   'y_coord',
]

DB_COLUMNS = [
   'NAME',
   'LOCATION',
   'SUB_LOCATION',
   'DESCRIPTION',
   'MENU_LINK',
   'X_COORD',
   'Y_COORD',
]

DATA_FILE = 'restaurant.json'

SQL_FILE = 'restaurant.sql'


class RestaurantSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='Restaurant',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


restaurants = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
