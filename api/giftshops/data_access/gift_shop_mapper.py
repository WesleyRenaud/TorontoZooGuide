from __future__ import annotations

from .gift_shop_record import GiftShopRecord
from ...types import Row


class GiftShopMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GiftShopRecord:
      return GiftShopRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         weekday_multiplier=row[ 'GIFT_SHOP_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ],
         weekend_holiday_multiplier=row[ 'GIFT_SHOP_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GiftShopRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
