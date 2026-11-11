from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'name',
   'location',
   'description',
   'x_coord',
   'y_coord',
   'closed_for_season_until_month',
   'weekday_start_month',
   'weekday_end_month',
   'weekend_start_month',
   'weekend_end_month',
]

DB_COLUMNS = [
   'NAME',
   'LOCATION',
   'DESCRIPTION',
   'X_COORD',
   'Y_COORD',
   'CLOSED_FOR_SEASON_UNTIL_MONTH',
   'WEEKDAY_START_MONTH',
   'WEEKDAY_END_MONTH',
   'WEEKEND_START_MONTH',
   'WEEKEND_END_MONTH',
]

DATA_FILE = 'gift_shop.json'

SQL_FILE = 'gift_shop.sql'


class GiftShopSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='GiftShop',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


gift_shops = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
