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
   'name',
   'enclosure_type',
   'seasonally_off_display_message',
   'x_coord',
   'y_coord',
   'default_itinerary_duration_minutes',
   'is_zoomobile_only',
]

DB_COLUMNS = [
   'SPECIES',
   'EXHIBIT',
   'NAME',
   'ENCLOSURE_TYPE',
   'SEASONALLY_OFF_DISPLAY_MESSAGE',
   'X_COORD',
   'Y_COORD',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
   'IS_ZOOMOBILE_ONLY',
]

DATA_FILE = 'enclosure_viewing.json'

SQL_FILE = 'enclosure_viewing.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='EnclosureViewing',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


enclosure_viewings = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
