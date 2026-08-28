from __future__ import annotations

from .guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from ...shared.calendar_dates import DateValues
from ...types import Types


class GuardiansTalkScheduleEndBuilder():
   @classmethod
   def build(
         cls,
         talk: str,
         location: str,
         schedule_end_date: Types.DateInput,
         talk_time: str ) -> GuardiansTalkScheduleEndInput:
      if not schedule_end_date:
         schedule_end_date = DateValues.today_date_key()

      return GuardiansTalkScheduleEndInput(
         talk_name=talk,
         location=location,
         schedule_end_date=schedule_end_date,
         talk_time=talk_time )
