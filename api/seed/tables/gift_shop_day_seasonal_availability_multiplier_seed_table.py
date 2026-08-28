from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


ENTITY_FIELDS = ( 'gift_shop', )
DAY_FIELDS = ( 'month', 'day', 'weekday', 'weekend_holiday' )

DB_COLUMNS = [
   'GIFT_SHOP',
   'MONTH',
   'DAY',
   'WEEKDAY_VALUE',
   'WEEKEND_HOLIDAY_VALUE',
]

GIFT_SHOP_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA = (
   'gift_shop_day_seasonal_availability_multiplier'
)

GIFT_SHOP_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL = (
   'gift_shop_day_seasonal_availability_multiplier.sql'
)


class GiftShopDaySeasonalAvailabilityMultiplierSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file(
         cursor,
         SeedSqlLoader.seed_sql_path( GIFT_SHOP_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_SQL ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_day_curve_directory(
         cursor,
         table='GiftShopDaySeasonalAvailabilityMultiplier',
         columns=DB_COLUMNS,
         directory=JsonSeedLoader.seed_data_dir( GIFT_SHOP_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
         entity_fields=ENTITY_FIELDS,
         day_fields=DAY_FIELDS )


gift_shop_day_seasonal_availability_multipliers = JsonSeedLoader.load_day_curve_directory(
   JsonSeedLoader.seed_data_dir( GIFT_SHOP_DAY_SEASONAL_AVAILABILITY_MULTIPLIER_DATA ),
   entity_fields=ENTITY_FIELDS,
   day_fields=DAY_FIELDS )
