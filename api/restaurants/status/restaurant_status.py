from __future__ import annotations

from ..scheduling.restaurant_opening_schedule import RestaurantOpeningSchedule
from ..scheduling.restaurant_schedule_override import RestaurantScheduleOverride
from ...shared.build_amenity_status_builders import AmenityStatusBuilders
from ...types import DateInput


_builders = AmenityStatusBuilders(
   name_field='restaurant',
   opening_schedule_class=RestaurantOpeningSchedule,
   schedule_override_class=RestaurantScheduleOverride,
)


def build_restaurant_closed_schedule(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantOpeningSchedule:
   return _builders.build_closed_schedule( restaurant, start_date, end_date, message )


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
   return _builders.build_opening_schedule(
      restaurant,
      start_date,
      end_date,
      monday,
      tuesday,
      wednesday,
      thursday,
      friday,
      saturday,
      sunday,
      holidays_only,
      message )


def build_restaurant_closure_override(
      restaurant: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestaurantScheduleOverride:
   return _builders.build_closure_override( restaurant, start_date, end_date, message )


__all__ = [
   'build_restaurant_closed_schedule',
   'build_restaurant_opening_schedule',
   'build_restaurant_closure_override',
]
