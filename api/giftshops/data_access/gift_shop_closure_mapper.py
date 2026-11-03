from __future__ import annotations

from .gift_shop_closure_record import GiftShopClosureRecord
from ...types import Types


class GiftShopClosureMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GiftShopClosureRecord:
      return GiftShopClosureRecord(
         gift_shop=row[ 'GIFT_SHOP' ],
         closed_start=row[ 'CLOSED_START' ],
         closed_end=row[ 'CLOSED_END' ],
         closed_message=row[ 'CLOSED_MESSAGE' ],
         is_closed_for_season=bool( row[ 'CLOSED_FOR_SEASON' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GiftShopClosureRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
