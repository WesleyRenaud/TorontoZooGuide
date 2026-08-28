from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


ENTITY_FIELDS = ( 'species', 'exhibit' )
DAY_FIELDS = ( 'month', 'day', 'value' )

DB_COLUMNS = [
   'SPECIES',
   'EXHIBIT',
   'MONTH',
   'DAY',
   'VALUE',
]

ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_DATA = (
   'animal_day_seasonal_viewability_multiplier'
)

ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_SQL = (
   'animal_day_seasonal_viewability_multiplier.sql'
)


class AnimalDaySeasonalViewabilityMultiplierSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file(
         cursor,
         SeedSqlLoader.seed_sql_path( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_SQL ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_day_curve_directory(
         cursor,
         table='AnimalDaySeasonalViewabilityMultiplier',
         columns=DB_COLUMNS,
         directory=JsonSeedLoader.seed_data_dir( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_DATA ),
         entity_fields=ENTITY_FIELDS,
         day_fields=DAY_FIELDS )


animal_day_seasonal_viewability_multipliers = JsonSeedLoader.load_day_curve_directory(
   JsonSeedLoader.seed_data_dir( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
