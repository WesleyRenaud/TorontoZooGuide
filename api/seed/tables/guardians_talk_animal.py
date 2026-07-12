from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'talk_name',
   'location',
   'species',
   'exhibit',
]

DB_COLUMNS = [
   'TALK_NAME',
   'LOCATION',
   'SPECIES',
   'EXHIBIT',
]

DATA_FILE = 'guardians_talk_animal.json'

SQL_FILE = 'guardians_talk_animal.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='GuardiansTalkAnimal',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


guardians_talk_animals = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
