from __future__ import annotations

from ..app_string_provider import AppStringProvider
from .calendar_dates import DateValues
from .opening_schedule_weekday_fields import OpeningScheduleWeekdayFields
from ..types import Types


class ClosedOpeningScheduleFieldsBuilder():
   @classmethod
   def build(
         cls,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> OpeningScheduleWeekdayFields:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format( 'guestStatus.locations.temporarilyClosed', name=name )

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
