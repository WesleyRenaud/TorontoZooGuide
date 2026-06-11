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


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='Restaurant',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


restaurants = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
