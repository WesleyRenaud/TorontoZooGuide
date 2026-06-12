from __future__ import annotations

from .attraction_opening_schedule import AttractionOpeningSchedule
from .attraction_schedule_override import AttractionScheduleOverride
from ...shared.build_amenity_status_builders import AmenityStatusBuilders
from ...types import DateInput


_builders = AmenityStatusBuilders(
   name_field='attraction',
   opening_schedule_class=AttractionOpeningSchedule,
   schedule_override_class=AttractionScheduleOverride,
)


def build_attraction_closed_schedule(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionOpeningSchedule:
   return _builders.build_closed_schedule( attraction, start_date, end_date, message )


def build_attraction_opening_schedule(
      attraction: str,
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
      message: str ) -> AttractionOpeningSchedule:
   return _builders.build_opening_schedule(
      attraction,
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


def build_attraction_closure_override(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionScheduleOverride:
   return _builders.build_closure_override( attraction, start_date, end_date, message )


__all__ = [
   'build_attraction_closed_schedule',
   'build_attraction_opening_schedule',
   'build_attraction_closure_override',
]
