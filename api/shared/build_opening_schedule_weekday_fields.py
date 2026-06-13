from __future__ import annotations

from .calendar_dates import DateValues
from .opening_schedule_weekday_fields import OpeningScheduleWeekdayFields
from .strings import SharedStrings
from ..types import DateInput


def build_opening_schedule_weekday_fields(
      name: str,
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
      message: str ) -> OpeningScheduleWeekdayFields:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.not_scheduled_to_be_open_today( name )

   return OpeningScheduleWeekdayFields(
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
