from __future__ import annotations

from ..json_seed_loader import insert_drinking_fountain_day_seasonal_curve_file
from ..json_seed_loader import load_drinking_fountain_day_seasonal_curve_file
from ..json_seed_loader import seed_data_path
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'drinking_fountain_day_seasonal_availability_multiplier.json'
)

DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'drinking_fountain_day_seasonal_availability_multiplier.sql'
)


def create_table( cursor: Cursor ) -> None:
   execute_sql_file(
      cursor,
      seed_sql_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_drinking_fountain_day_seasonal_curve_file(
      cursor,
      table='DrinkingFountainDaySeasonalAvailabilityMultiplier',
      path=seed_data_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ) )


drinking_fountain_day_seasonal_availability_multipliers = (
   load_drinking_fountain_day_seasonal_curve_file(
      seed_data_path( DRINKING_FOUNTAIN_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ) ) )
