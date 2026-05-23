from __future__ import annotations

from collections.abc import Iterable

from .gift_shop_record import GiftShopRecord
from .gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from .gift_shop_schedule_record import GiftShopScheduleRecord
from ...types import Row


def map_gift_shop_record( row: Row ) -> GiftShopRecord:
   return GiftShopRecord(
      name=row[ 'NAME' ],
      location=row[ 'LOCATION' ],
      description=row[ 'DESCRIPTION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      weekday_multiplier=row[ 'GIFT_SHOP_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ],
      weekend_holiday_multiplier=row[ 'GIFT_SHOP_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ] )


def map_gift_shop_records( rows: Iterable[ Row ] ) -> list[ GiftShopRecord ]:
   return [
      map_gift_shop_record( row )
      for row in rows
   ]


def map_gift_shop_schedule_record( row: Row ) -> GiftShopScheduleRecord:
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


def map_gift_shop_schedule_records( rows: Iterable[ Row ] ) -> list[ GiftShopScheduleRecord ]:
   return [
      map_gift_shop_schedule_record( row )
      for row in rows
   ]


def map_gift_shop_schedule_override_record( row: Row ) -> GiftShopScheduleOverrideRecord:
   return GiftShopScheduleOverrideRecord(
      gift_shop=row[ 'GIFT_SHOP' ],
      override_start_date=row[ 'OVERRIDE_START_DATE' ],
      override_end_date=row[ 'OVERRIDE_END_DATE' ],
      is_closed=row[ 'IS_CLOSED' ],
      override_message=row[ 'OVERRIDE_MESSAGE' ] )


def map_gift_shop_schedule_override_records( rows: Iterable[ Row ] ) -> list[ GiftShopScheduleOverrideRecord ]:
   return [
      map_gift_shop_schedule_override_record( row )
      for row in rows
   ]
