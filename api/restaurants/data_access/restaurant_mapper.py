from __future__ import annotations

from .restaurant_record import RestaurantRecord
from ...shared.peak_months import PeakMonths
from ...types import Types


class RestaurantMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> RestaurantRecord:
      return RestaurantRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         sub_location=row[ 'SUB_LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         menu_link=row[ 'MENU_LINK' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         peak_months=PeakMonths.from_row( row ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ RestaurantRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
