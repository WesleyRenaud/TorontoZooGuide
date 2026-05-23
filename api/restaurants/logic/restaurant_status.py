from __future__ import annotations

from ...zoo_util import ZooUtil
from ...shared.strings import SharedStrings
from ...types import DateInput
from .restaurant_opening_schedule import RestaurantOpeningSchedule
from .restaurant_schedule_override import RestaurantScheduleOverride


def build_restaurant_closed_schedule(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantOpeningSchedule:
   date_range = ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( restaurant )

   return RestaurantOpeningSchedule(
      restaurant=restaurant,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=message )


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
   date_range = ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.not_scheduled_to_be_open_today(
         restaurant )

   return RestaurantOpeningSchedule(
      restaurant=restaurant,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      holidays_only=holidays_only,
      message=message )


def build_restaurant_closure_override(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantScheduleOverride:
   date_range = ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( restaurant )

   return RestaurantScheduleOverride(
      restaurant=restaurant,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      is_closed=True,
      message=message )
