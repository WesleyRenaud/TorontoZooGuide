from __future__ import annotations

from ..json_seed_loader import insert_day_seasonal_value_curve_directory
from ..json_seed_loader import load_day_seasonal_value_curve_directory
from ..json_seed_loader import seed_data_dir
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'exhibit_day_seasonal_availability_multiplier'
)

EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'exhibit_day_seasonal_availability_multiplier.sql'
)


def create_table( cursor: Cursor ) -> None:
   execute_sql_file(
      cursor,
      seed_sql_path( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_day_seasonal_value_curve_directory(
      cursor,
      table='ExhibitDaySeasonalAvailabilityMultiplier',
      entity_column='EXHIBIT',
      entity_field='exhibit',
      directory=seed_data_dir( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ) )


exhibit_day_seasonal_availability_multipliers = (
   load_day_seasonal_value_curve_directory(
      seed_data_dir( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
      entity_field='exhibit' ) )
