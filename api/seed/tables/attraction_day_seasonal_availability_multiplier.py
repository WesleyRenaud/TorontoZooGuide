from __future__ import annotations

from ..json_seed_loader import insert_day_curve_directory
from ..json_seed_loader import load_day_curve_directory
from ..json_seed_loader import seed_data_dir
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


ENTITY_FIELDS = ( 'attraction', )
DAY_FIELDS = ( 'month', 'day', 'weekday', 'weekend_holiday' )

DB_COLUMNS = [
   'ATTRACTION',
   'MONTH',
   'DAY',
   'WEEKDAY_VALUE',
   'WEEKEND_HOLIDAY_VALUE',
]

ATTRACTION_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'attraction_day_seasonal_availability_multiplier'
)

ATTRACTION_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'attraction_day_seasonal_availability_multiplier.sql'
)


def create_table( cursor: Cursor ) -> None:
   execute_sql_file(
      cursor,
      seed_sql_path( ATTRACTION_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_day_curve_directory(
      cursor,
      table='AttractionDaySeasonalAvailabilityMultiplier',
      columns=DB_COLUMNS,
      directory=seed_data_dir( ATTRACTION_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
      entity_fields=ENTITY_FIELDS,
      day_fields=DAY_FIELDS )


attraction_day_seasonal_availability_multipliers = load_day_curve_directory(
   seed_data_dir( ATTRACTION_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
