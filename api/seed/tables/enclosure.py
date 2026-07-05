from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
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


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='Enclosure',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


enclosures = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
