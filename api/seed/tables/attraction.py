from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'name',
   'free_with_admission',
   'description',
   'info_link',
   'hyperlink_text',
   'x_coord',
   'y_coord',
   'default_itinerary_duration_minutes',
   'region',
]

DB_COLUMNS = [
   'NAME',
   'FREE_WITH_ADMISSION',
   'DESCRIPTION',
   'INFO_LINK',
   'HYPERLINK_TEXT',
   'X_COORD',
   'Y_COORD',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
   'REGION',
]

DATA_FILE = 'attraction.json'

SQL_FILE = 'attraction.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='Attraction',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


attractions = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
