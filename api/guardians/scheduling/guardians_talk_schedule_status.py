from __future__ import annotations

from .guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ...shared.calendar_dates import DateValues
from ...shared.strings import SharedStrings
from ...types import DateInput


def build_guardians_talk_schedule(
      talk: str,
      location: str,
      start_date: DateInput,
      end_date: DateInput,
      talk_time: str,
      monday: bool,
      tuesday: bool,
      wednesday: bool,
      thursday: bool,
      friday: bool,
      saturday: bool,
      sunday: bool,
      message: str ) -> GuardiansTalkScheduleInput:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.GuardiansTalks.not_scheduled_today(
         talk,
         location )

   return GuardiansTalkScheduleInput(
      talk_name=talk,
      location=location,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      talk_time=talk_time,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      message=message )
