from __future__ import annotations

from .gift_shop_schedule_record import GiftShopScheduleRecord
from ...types import Row


class GiftShopScheduleMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GiftShopScheduleRecord:
      return GiftShopScheduleRecord(
         gift_shop=row[ 'GIFT_SHOP' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         monday=row[ 'MONDAY' ],
         tuesday=row[ 'TUESDAY' ],
         wednesday=row[ 'WEDNESDAY' ],
         thursday=row[ 'THURSDAY' ],
         friday=row[ 'FRIDAY' ],
         saturday=row[ 'SATURDAY' ],
         sunday=row[ 'SUNDAY' ],
         holidays_only=row[ 'HOLIDAYS_ONLY' ],
         schedule_message=row[ 'SCHEDULE_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GiftShopScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
