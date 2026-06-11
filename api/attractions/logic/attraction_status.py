from __future__ import annotations

from .attraction_opening_schedule import AttractionOpeningSchedule
from .attraction_schedule_override import AttractionScheduleOverride
from ...shared.build_closed_opening_schedule_fields import build_closed_opening_schedule_fields
from ...shared.build_closure_override_fields import build_closure_override_fields
from ...shared.build_opening_schedule_weekday_fields import build_opening_schedule_weekday_fields
from ...types import DateInput


def build_attraction_closed_schedule(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionOpeningSchedule:
   fields = build_closed_opening_schedule_fields(
      name=attraction,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return AttractionOpeningSchedule(
      attraction=attraction,
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
   fields = build_opening_schedule_weekday_fields(
      name=attraction,
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

   return AttractionOpeningSchedule(
      attraction=attraction,
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


def build_attraction_closure_override(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionScheduleOverride:
   fields = build_closure_override_fields(
      name=attraction,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return AttractionScheduleOverride(
      attraction=attraction,
      start_date=fields.start_date,
      end_date=fields.end_date,
      is_closed=fields.is_closed,
      message=fields.message )
