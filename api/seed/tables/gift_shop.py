from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'name',
   'location',
   'description',
   'x_coord',
   'y_coord',
]

DB_COLUMNS = [
   'NAME',
   'LOCATION',
   'DESCRIPTION',
   'X_COORD',
   'Y_COORD',
]

DATA_FILE = 'gift_shop.json'

SQL_FILE = 'gift_shop.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='GiftShop',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


gift_shops = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
