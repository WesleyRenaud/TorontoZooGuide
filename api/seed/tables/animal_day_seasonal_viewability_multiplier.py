from __future__ import annotations

from ..json_seed_loader import insert_day_curve_directory
from ..json_seed_loader import load_day_curve_directory
from ..json_seed_loader import seed_data_dir
from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


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


def create_table( cursor: Cursor ) -> None:
   execute_sql_file(
      cursor,
      seed_sql_path( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_SQL ) )


def insert_rows( cursor: Cursor ) -> None:
   insert_day_curve_directory(
      cursor,
      table='AnimalDaySeasonalViewabilityMultiplier',
      columns=DB_COLUMNS,
      directory=seed_data_dir( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_DATA ),
      entity_fields=ENTITY_FIELDS,
      day_fields=DAY_FIELDS )


animal_day_seasonal_viewability_multipliers = load_day_curve_directory(
   seed_data_dir( ANIMAL_DAY_SEASONAL_VIEWABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
