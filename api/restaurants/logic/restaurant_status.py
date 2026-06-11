from __future__ import annotations

from .restaurant_opening_schedule import RestaurantOpeningSchedule
from .restaurant_schedule_override import RestaurantScheduleOverride
from ...shared.build_closed_opening_schedule_fields import build_closed_opening_schedule_fields
from ...shared.build_closure_override_fields import build_closure_override_fields
from ...shared.build_opening_schedule_weekday_fields import build_opening_schedule_weekday_fields
from ...types import DateInput


def build_restaurant_closed_schedule(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantOpeningSchedule:
   fields = build_closed_opening_schedule_fields(
      name=restaurant,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return RestaurantOpeningSchedule(
      restaurant=restaurant,
      start_date=fields.start_date,
      end_date=fields.end_date,
      monday=fields.monday,
      tuesday=fields.tuesday,
      wednesday=fields.wednesday,
      thursday=fields.thursday,
      friday=fields.friday,
      saturday=fields.saturday,
      sunday=fields.sunday,
      holidays_only=fields.holidays_only,
      message=fields.message )


def build_restaurant_opening_schedule(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      monday: bool,
      tuesday: bool,
      wednesday: bool,
      thursday: bool,
      friday: bool,
      saturday: bool,
      sunday: bool,
      holidays_only: bool,
      message: str ) -> RestaurantOpeningSchedule:
   fields = build_opening_schedule_weekday_fields(
      name=restaurant,
      start_date=start_date,
      end_date=end_date,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      holidays_only=holidays_only,
      message=message )

   return RestaurantOpeningSchedule(
      restaurant=restaurant,
      start_date=fields.start_date,
      end_date=fields.end_date,
      monday=fields.monday,
      tuesday=fields.tuesday,
      wednesday=fields.wednesday,
      thursday=fields.thursday,
      friday=fields.friday,
      saturday=fields.saturday,
      sunday=fields.sunday,
      holidays_only=fields.holidays_only,
      message=fields.message )


def build_restaurant_closure_override(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantScheduleOverride:
   fields = build_closure_override_fields(
      name=restaurant,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return RestaurantScheduleOverride(
      restaurant=restaurant,
      start_date=fields.start_date,
      end_date=fields.end_date,
      is_closed=fields.is_closed,
      message=fields.message )
