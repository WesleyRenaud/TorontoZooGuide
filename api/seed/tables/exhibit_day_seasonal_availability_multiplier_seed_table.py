from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


ENTITY_FIELDS = ( 'exhibit', )
DAY_FIELDS = ( 'month', 'day', 'value' )

DB_COLUMNS = [
   'EXHIBIT',
   'MONTH',
   'DAY',
   'VALUE',
]

EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'exhibit_day_seasonal_availability_multiplier'
)

EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'exhibit_day_seasonal_availability_multiplier.sql'
)


class ExhibitDaySeasonalAvailabilityMultiplierSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file(
         cursor,
         SeedSqlLoader.seed_sql_path( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_day_curve_directory(
         cursor,
         table='ExhibitDaySeasonalAvailabilityMultiplier',
         columns=DB_COLUMNS,
         directory=JsonSeedLoader.seed_data_dir( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
         entity_fields=ENTITY_FIELDS,
         day_fields=DAY_FIELDS )


exhibit_day_seasonal_availability_multipliers = JsonSeedLoader.load_day_curve_directory(
   JsonSeedLoader.seed_data_dir( EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
