from __future__ import annotations

from ..json_seed_loader import insert_day_seasonal_availability_curve_directory
from ..json_seed_loader import load_day_seasonal_availability_curve_directory
from ..json_seed_loader import seed_data_dir
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'restaurant_day_seasonal_availability_multiplier'
)

RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'restaurant_day_seasonal_availability_multiplier.sql'
)


def create_table( cursor: Cursor ) -> None:
   execute_sql_file(
      cursor,
      seed_sql_path( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_day_seasonal_availability_curve_directory(
      cursor,
      table='RestaurantDaySeasonalAvailabilityMultiplier',
      entity_column='RESTAURANT',
      entity_field='restaurant',
      directory=seed_data_dir( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ) )


restaurant_day_seasonal_availability_multipliers = (
   load_day_seasonal_availability_curve_directory(
      seed_data_dir( RESTAURANT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
      entity_field='restaurant' ) )
