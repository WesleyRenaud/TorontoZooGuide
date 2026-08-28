from __future__ import annotations

from .gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from ...types import Types


class GiftShopScheduleOverrideMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GiftShopScheduleOverrideRecord:
      return GiftShopScheduleOverrideRecord(
         gift_shop=row[ 'GIFT_SHOP' ],
         override_start_date=row[ 'OVERRIDE_START_DATE' ],
         override_end_date=row[ 'OVERRIDE_END_DATE' ],
         is_closed=row[ 'IS_CLOSED' ],
         override_message=row[ 'OVERRIDE_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GiftShopScheduleOverrideRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
