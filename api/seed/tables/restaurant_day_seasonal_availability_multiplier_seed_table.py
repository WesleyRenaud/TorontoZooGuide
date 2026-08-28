from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


ENTITY_FIELDS = ( 'restaurant', )
DAY_FIELDS = ( 'month', 'day', 'weekday', 'weekend_holiday' )

DB_COLUMNS = [
   'RESTAURANT',
   'MONTH',
   'DAY',
   'WEEKDAY_VALUE',
   'WEEKEND_HOLIDAY_VALUE',
]

RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'restaurant_day_seasonal_availability_multiplier'
)

RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'restaurant_day_seasonal_availability_multiplier.sql'
)


class RestaurantDaySeasonalAvailabilityMultiplierSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file(
         cursor,
         SeedSqlLoader.seed_sql_path( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_day_curve_directory(
         cursor,
         table='RestaurantDaySeasonalAvailabilityMultiplier',
         columns=DB_COLUMNS,
         directory=JsonSeedLoader.seed_data_dir( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
         entity_fields=ENTITY_FIELDS,
         day_fields=DAY_FIELDS )


restaurant_day_seasonal_availability_multipliers = JsonSeedLoader.load_day_curve_directory(
   JsonSeedLoader.seed_data_dir( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
