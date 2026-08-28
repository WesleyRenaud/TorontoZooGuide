from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'attraction',
   'species',
   'exhibit',
   'enclosure_name',
]

DB_COLUMNS = [
   'ATTRACTION',
   'SPECIES',
   'EXHIBIT',
   'ENCLOSURE_NAME',
]

DATA_FILE = 'attraction_animal.json'

SQL_FILE = 'attraction_animal.sql'


class AttractionAnimalSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='AttractionAnimal',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


attraction_animals = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
