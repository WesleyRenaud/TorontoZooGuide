from __future__ import annotations

from ..json_seed_loader import insert_json_records
from ..json_seed_loader import load_json_records
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RECORD_FIELDS = [
   'species',
   'latin_name',
   'min_temperature',
   'general_viewing_tips',
   'seasonal_viewing_tips',
   'identification',
   'habitat_and_range',
   'diet_and_feeding',
   'behaviour_and_social_life',
   'adaptations',
   'reproduction_and_life_cycle',
   'animals_at_the_zoo',
]

DB_COLUMNS = [
   'SPECIES',
   'LATIN_NAME',
   'MIN_TEMPERATURE',
   'GENERAL_VIEWING_TIPS',
   'SEASONAL_VIEWING_TIPS',
   'IDENTIFICATION',
   'HABITAT_AND_RANGE',
   'DIET_AND_FEEDING',
   'BEHAVIOUR_AND_SOCIAL_LIFE',
   'ADAPTATIONS',
   'REPRODUCTION_AND_LIFE_CYCLE',
   'ANIMALS_AT_THE_ZOO',
]

DATA_FILE = 'animal.json'

SQL_FILE = 'animal.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_json_records(
      cursor,
      table='Animal',
      columns=DB_COLUMNS,
      fields=RECORD_FIELDS,
      path=seed_data_path( DATA_FILE ) )


animals = load_json_records(
   seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
