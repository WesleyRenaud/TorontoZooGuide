from __future__ import annotations

from .attraction_opening_schedule import AttractionOpeningSchedule
from .attraction_schedule_override import AttractionScheduleOverride
from ...shared.date_values import DateValues
from ...shared.strings import SharedStrings
from ...types import DateInput


def build_attraction_closed_schedule(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionOpeningSchedule:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( attraction )

   return AttractionOpeningSchedule(
      attraction=attraction,
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
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.not_scheduled_to_be_open_today(
         attraction )

   return AttractionOpeningSchedule(
      attraction=attraction,
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


def build_attraction_closure_override(
      attraction: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> AttractionScheduleOverride:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( attraction )

   return AttractionScheduleOverride(
      attraction=attraction,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      is_closed=True,
      message=message )
