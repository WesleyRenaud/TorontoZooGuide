from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'name',
   'meeting_spot',
   'link',
   'maximum_duration',
]

DB_COLUMNS = [
   'NAME',
   'MEETING_SPOT',
   'LINK',
   'MAXIMUM_DURATION',
]

DATA_FILE = 'wild_encounter.json'

SQL_FILE = 'wild_encounter.sql'


class WildEncounterSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='WildEncounter',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


wild_encounters = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
