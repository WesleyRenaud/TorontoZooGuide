from __future__ import annotations

from .restaurant_mapper import map_restaurant_records
from .restaurant_mapper import map_restaurant_schedule_override_records
from .restaurant_mapper import map_restaurant_schedule_records
from .restaurant_record import RestaurantRecord
from .restaurant_schedule_override_record import RestaurantScheduleOverrideRecord
from .restaurant_schedule_record import RestaurantScheduleRecord
from ...types import Connection, VisitDay, VisitMonth


def fetch_restaurant_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  r.NAME
               FROM Restaurant r;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_restaurant_records(
      conn: Connection,
      month: VisitMonth,
      day: VisitDay ) -> list[ RestaurantRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  r.NAME,
                  r.LOCATION,
                  r.SUB_LOCATION,
                  r.DESCRIPTION,
                  r.MENU_LINK,
                  r.X_COORD,
                  r.Y_COORD,
                  COALESCE( rdsam.WEEKDAY_VALUE, 1.0 ) AS RESTAURANT_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( rdsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS RESTAURANT_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM Restaurant r
               LEFT JOIN RestaurantDaySeasonalAvailabilityMultiplier rdsam
                  ON r.NAME = rdsam.RESTAURANT
                  AND rdsam.MONTH = ?
                  AND rdsam.DAY = ?;
         """, ( month, day ) )

      return map_restaurant_records( data.fetchall() )

   finally:
      cur.close()


def fetch_restaurant_schedule_records( conn: Connection ) -> list[ RestaurantScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.RESTAURANT,
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
               FROM RestaurantOpeningSchedule s;
         """ )

      return map_restaurant_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_restaurant_schedule_override_records(
      conn: Connection ) -> list[ RestaurantScheduleOverrideRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  o.RESTAURANT,
                  o.OVERRIDE_START_DATE,
                  o.OVERRIDE_END_DATE,
                  o.IS_CLOSED,
                  o.OVERRIDE_MESSAGE
               FROM RestaurantScheduleOverride o;
         """ )

      return map_restaurant_schedule_override_records( data.fetchall() )

   finally:
      cur.close()
