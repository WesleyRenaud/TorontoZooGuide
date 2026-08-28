from __future__ import annotations

from ...app_string_provider import AppStringProvider
from .guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ...shared.calendar_dates import DateValues
from ...types import Types


class GuardiansTalkScheduleBuilder():
   @classmethod
   def build(
         cls,
         talk: str,
         location: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
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
         message = AppStringProvider.format(
            'guestStatus.guardiansTalks.notScheduledToday',
            talkName=talk,
            location=location )

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
