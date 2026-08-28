from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


DAY_FIELDS = ( 'month', 'day', 'likelihood' )

DB_COLUMNS = [
   'MONTH',
   'DAY',
   'LIKELIHOOD',
]

DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'drinking_fountain_day_seasonal_availability_multiplier.json'
)

DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'drinking_fountain_day_seasonal_availability_multiplier.sql'
)


class DrinkingFountainDaySeasonalAvailabilityMultiplierSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file(
         cursor,
         SeedSqlLoader.seed_sql_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_day_curve_file(
         cursor,
         table='DrinkingFountainDaySeasonalAvailabilityMultiplier',
         columns=DB_COLUMNS,
         path=JsonSeedLoader.seed_data_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
         day_fields=DAY_FIELDS )


drinking_fountain_day_seasonal_availability_multipliers = JsonSeedLoader.load_day_curve_file(
   JsonSeedLoader.seed_data_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
   day_fields=DAY_FIELDS )
