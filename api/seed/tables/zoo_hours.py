from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
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


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='ZooHours',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


zoo_hours = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
