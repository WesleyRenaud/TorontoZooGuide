from __future__ import annotations

from .restaurant_record import RestaurantRecord
from ...types import Row


class RestaurantMapper():
   @classmethod
   def map_record( cls, row: Row ) -> RestaurantRecord:
      return RestaurantRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         sub_location=row[ 'SUB_LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         menu_link=row[ 'MENU_LINK' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         weekday_multiplier=row[ 'RESTAURANT_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ],
         weekend_holiday_multiplier=row[ 'RESTAURANT_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ RestaurantRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
