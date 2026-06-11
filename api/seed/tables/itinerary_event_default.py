from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'event_type',
   'default_itinerary_duration_minutes',
]

DB_COLUMNS = [
   'EVENT_TYPE',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
]

DATA_FILE = 'itinerary_event_default.json'

SQL_FILE = 'itinerary_event_default.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='ItineraryEventDefault',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


itinerary_event_defaults = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
