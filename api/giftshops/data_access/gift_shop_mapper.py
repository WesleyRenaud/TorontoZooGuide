from __future__ import annotations

from .gift_shop_record import GiftShopRecord
from ...shared.peak_months import PeakMonths
from ...types import Types


class GiftShopMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GiftShopRecord:
      return GiftShopRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         peak_months=PeakMonths.from_row( row ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GiftShopRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
