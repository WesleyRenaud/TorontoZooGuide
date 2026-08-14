from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'transportation',
   'from_station',
   'to_station',
   'duration_minutes',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'FROM_STATION',
   'TO_STATION',
   'DURATION_MINUTES',
]

DATA_FILE = 'transportation_leg.json'

SQL_FILE = 'transportation_leg.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='TransportationLeg',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


transportation_legs = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
