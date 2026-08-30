from __future__ import annotations

from datetime import date

from api.restaurants.data_access.restaurant_record import RestaurantRecord
from api.restaurants.data_access.restaurant_schedule_record import RestaurantScheduleRecord
from api.restaurants.domain.restaurant_builder import RestaurantBuilder
from api.shared.enums.schedule_status import ScheduleStatus
from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext


RESTAURANT_NAME = 'Africa Restaurant'
OTHER_RESTAURANT_NAME = 'Beavertails'
CUSTOM_CLOSED_MESSAGE = 'Closed for testing.'
VISIT_DATE = date( 2026, 6, 15 )


def _visit_context() -> OpeningScheduleVisitContext:
   return OpeningScheduleVisitContext(
      normalized_month=VISIT_DATE.month,
      normalized_day=VISIT_DATE.day,
      target_date=VISIT_DATE,
      weekday=VISIT_DATE.weekday(),
      is_weekend_or_holiday=False )


def _restaurant_record( **overrides: object ) -> RestaurantRecord:
   values: dict[ str, object ] = {
      'name': RESTAURANT_NAME,
      'location': 'Africa',
      'sub_location': None,
      'description': 'Restaurant',
      'menu_link': None,
      'x_coord': 1.0,
      'y_coord': 2.0,
      'weekday_multiplier': 1.0,
      'weekend_holiday_multiplier': 1.0,
   }
   values.update( overrides )

   return RestaurantRecord( **values )


def _schedule_record( **overrides: object ) -> RestaurantScheduleRecord:
   values: dict[ str, object ] = {
      'restaurant': RESTAURANT_NAME,
      'schedule_start_date': '2026-06-01',
      'schedule_end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'schedule_message': CUSTOM_CLOSED_MESSAGE,
   }
   values.update( overrides )

   return RestaurantScheduleRecord( **values )


def Test_CalculateLikelihood_TestSeasonalMultiplier_ExpectClampedAndRounded() -> None:
   assert RestaurantBuilder.calculate_likelihood( None ) == 100
   assert RestaurantBuilder.calculate_likelihood( -0.5 ) == 0
   assert RestaurantBuilder.calculate_likelihood( 0.444 ) == 44
   assert RestaurantBuilder.calculate_likelihood( 1.5 ) == 100


def Test_GetActiveScheduleStatus_TestOpenMonday_ExpectOpen() -> None:
   status, message = RestaurantBuilder.get_active_schedule_status(
      schedule_records=[ _schedule_record( monday=True ) ],
      target_date=VISIT_DATE,
      weekday=VISIT_DATE.weekday() )

   assert status == ScheduleStatus.OPEN
   assert message is None


def Test_GetActiveScheduleStatus_TestClosedMonday_ExpectClosedMessage() -> None:
   status, message = RestaurantBuilder.get_active_schedule_status(
      schedule_records=[ _schedule_record() ],
      target_date=VISIT_DATE,
      weekday=VISIT_DATE.weekday() )

   assert status == ScheduleStatus.CLOSED
   assert message == CUSTOM_CLOSED_MESSAGE


def Test_BuildRestaurants_TestClosedRestaurant_ExpectExcludedUnlessIncludedOrListed() -> None:
   context = _visit_context()
   closed_record = _restaurant_record( weekday_multiplier=0, weekend_holiday_multiplier=0 )
   schedule_records = [ _schedule_record() ]

   open_only = RestaurantBuilder.build_restaurants(
      restaurant_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_restaurants=False )
   with_closed = RestaurantBuilder.build_restaurants(
      restaurant_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_restaurants=True )
   explicitly_listed = RestaurantBuilder.build_restaurants(
      restaurant_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_restaurants=False,
      restaurants_to_include=[ RESTAURANT_NAME ] )

   assert open_only == []
   assert len( with_closed ) == 1
   assert with_closed[ 0 ].is_closed is True
   assert len( explicitly_listed ) == 1
   assert explicitly_listed[ 0 ].name == RESTAURANT_NAME


def Test_BuildRestaurant_TestClosedSchedule_ExpectCustomClosedMessage() -> None:
   restaurant = RestaurantBuilder.build_restaurant(
      restaurant_record=_restaurant_record(),
      schedule_records=[ _schedule_record() ],
      schedule_override_records=[],
      context=_visit_context() )

   assert restaurant.is_closed is True
   assert restaurant.closed_message == CUSTOM_CLOSED_MESSAGE
