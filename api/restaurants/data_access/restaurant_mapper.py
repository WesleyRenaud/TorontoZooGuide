from .restaurant_record import RestaurantRecord
from .restaurant_schedule_record import RestaurantScheduleRecord


def map_restaurant_record( row ):
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


def map_restaurant_records( rows ):
   return [
      map_restaurant_record( row )
      for row in rows
   ]


def map_restaurant_schedule_record( row ):
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


def map_restaurant_schedule_records( rows ):
   return [
      map_restaurant_schedule_record( row )
      for row in rows
   ]
