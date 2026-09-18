from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'transportation',
   'from_station',
   'to_station',
   'species',
   'exhibit',
   'enclosure_name',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'FROM_STATION',
   'TO_STATION',
   'SPECIES',
   'EXHIBIT',
   'ENCLOSURE_NAME',
]

DATA_FILE = 'transportation_animal.json'

SQL_FILE = 'transportation_animal.sql'


class TransportationAnimalSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='TransportationAnimal',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


transportation_animals = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
