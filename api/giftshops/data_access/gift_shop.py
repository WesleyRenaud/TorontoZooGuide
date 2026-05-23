from __future__ import annotations

from ...types import Connection, VisitDay, VisitMonth
from .gift_shop_mapper import map_gift_shop_records
from .gift_shop_mapper import map_gift_shop_schedule_override_records
from .gift_shop_mapper import map_gift_shop_schedule_records
from .gift_shop_record import GiftShopRecord
from .gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from .gift_shop_schedule_record import GiftShopScheduleRecord


def fetch_gift_shop_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  g.NAME
               FROM GiftShop g;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_gift_shop_records(
      conn: Connection,
      month: VisitMonth,
      day: VisitDay ) -> list[ GiftShopRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  g.NAME,
                  g.LOCATION,
                  g.DESCRIPTION,
                  g.X_COORD,
                  g.Y_COORD,
                  COALESCE( gdsam.WEEKDAY_VALUE, 1.0 ) AS GIFT_SHOP_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( gdsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS GIFT_SHOP_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM GiftShop g
               LEFT JOIN GiftShopDaySeasonalAvailabilityMultiplier gdsam
                  ON g.NAME = gdsam.GIFT_SHOP
                  AND gdsam.MONTH = ?
                  AND gdsam.DAY = ?;
         """, ( month, day ) )

      return map_gift_shop_records( data.fetchall() )

   finally:
      cur.close()


def fetch_gift_shop_schedule_records( conn: Connection ) -> list[ GiftShopScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.GIFT_SHOP,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.HOLIDAYS_ONLY,
                  s.SCHEDULE_MESSAGE
               FROM GiftShopOpeningSchedule s;
         """ )

      return map_gift_shop_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_gift_shop_schedule_override_records(
      conn: Connection ) -> list[ GiftShopScheduleOverrideRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  o.GIFT_SHOP,
                  o.OVERRIDE_START_DATE,
                  o.OVERRIDE_END_DATE,
                  o.IS_CLOSED,
                  o.OVERRIDE_MESSAGE
               FROM GiftShopScheduleOverride o;
         """ )

      return map_gift_shop_schedule_override_records( data.fetchall() )

   finally:
      cur.close()
