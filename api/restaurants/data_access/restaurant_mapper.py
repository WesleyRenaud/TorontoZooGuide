from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .restaurant_record import RestaurantRecord
from .restaurant_schedule_override_record import RestaurantScheduleOverrideRecord
from .restaurant_schedule_record import RestaurantScheduleRecord


def map_restaurant_record( row: Row ) -> RestaurantRecord:
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


def map_restaurant_records( rows: Iterable[ Row ] ) -> list[ RestaurantRecord ]:
   return [
      map_restaurant_record( row )
      for row in rows
   ]


def map_restaurant_schedule_record( row: Row ) -> RestaurantScheduleRecord:
   return RestaurantScheduleRecord(
      restaurant=row[ 'RESTAURANT' ],
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


def map_restaurant_schedule_records( rows: Iterable[ Row ] ) -> list[ RestaurantScheduleRecord ]:
   return [
      map_restaurant_schedule_record( row )
      for row in rows
   ]


def map_restaurant_schedule_override_record( row: Row ) -> RestaurantScheduleOverrideRecord:
   return RestaurantScheduleOverrideRecord(
      restaurant=row[ 'RESTAURANT' ],
      override_start_date=row[ 'OVERRIDE_START_DATE' ],
      override_end_date=row[ 'OVERRIDE_END_DATE' ],
      is_closed=row[ 'IS_CLOSED' ],
      override_message=row[ 'OVERRIDE_MESSAGE' ] )


def map_restaurant_schedule_override_records( rows: Iterable[ Row ] ) -> list[ RestaurantScheduleOverrideRecord ]:
   return [
      map_restaurant_schedule_override_record( row )
      for row in rows
   ]
