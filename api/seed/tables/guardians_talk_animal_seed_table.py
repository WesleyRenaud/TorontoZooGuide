from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'talk_name',
   'location',
   'species',
   'exhibit',
   'enclosure_name',
]

DB_COLUMNS = [
   'TALK_NAME',
   'LOCATION',
   'SPECIES',
   'EXHIBIT',
   'ENCLOSURE_NAME',
]

DATA_FILE = 'guardians_talk_animal.json'

SQL_FILE = 'guardians_talk_animal.sql'


class GuardiansTalkAnimalSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='GuardiansTalkAnimal',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


guardians_talk_animals = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
