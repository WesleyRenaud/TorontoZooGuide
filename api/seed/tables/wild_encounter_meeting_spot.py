from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'name',
   'x_coord',
   'y_coord',
   'loop_id',
   'loop_viewing_spot_index',
]

DB_COLUMNS = [
   'NAME',
   'X_COORD',
   'Y_COORD',
   'LOOP_ID',
   'LOOP_VIEWING_SPOT_INDEX',
]

DATA_FILE = 'wild_encounter_meeting_spot.json'

SQL_FILE = 'wild_encounter_meeting_spot.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='WildEncounterMeetingSpot',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


wild_encounter_meeting_spots = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
