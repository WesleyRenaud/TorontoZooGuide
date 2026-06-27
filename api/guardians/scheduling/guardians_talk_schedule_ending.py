from __future__ import annotations

from .guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from ...shared.calendar_dates import DateValues
from ...types import DateInput


def build_guardians_talk_schedule_end(
      talk: str,
      location: str,
      schedule_end_date: DateInput ) -> GuardiansTalkScheduleEndInput:
   if not schedule_end_date:
      schedule_end_date = DateValues.today_date_key()

   return GuardiansTalkScheduleEndInput(
      talk_name=talk,
      location=location,
      schedule_end_date=schedule_end_date )
