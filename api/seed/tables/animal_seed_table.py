from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


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


class AnimalSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='Animal',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


animals = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
