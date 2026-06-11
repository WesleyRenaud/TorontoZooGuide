from __future__ import annotations

from .date_values import DateValues
from .opening_schedule_weekday_fields import OpeningScheduleWeekdayFields
from .strings import SharedStrings
from ..types import DateInput


def build_closed_opening_schedule_fields(
      name: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> OpeningScheduleWeekdayFields:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( name )

   return OpeningScheduleWeekdayFields(
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
