from __future__ import annotations

from ...zoo_util import ZooUtil
from ...shared.strings import SharedStrings
from ...types import DateInput, ScheduleTimeKey
from .guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from .guardians_talk_schedule_input import GuardiansTalkScheduleInput


def build_guardians_talk_schedule(
      talk: str,
      location: str,
      start_date: DateInput,
      end_date: DateInput,
      monday_time: ScheduleTimeKey,
      tuesday_time: ScheduleTimeKey,
      wednesday_time: ScheduleTimeKey,
      thursday_time: ScheduleTimeKey,
      friday_time: ScheduleTimeKey,
      saturday_time: ScheduleTimeKey,
      sunday_time: ScheduleTimeKey,
      message: str ) -> GuardiansTalkScheduleInput:
   date_range = ZooUtil.resolve_open_ended_date_range(
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
      monday_time=monday_time,
      tuesday_time=tuesday_time,
      wednesday_time=wednesday_time,
      thursday_time=thursday_time,
      friday_time=friday_time,
      saturday_time=saturday_time,
      sunday_time=sunday_time,
      message=message )


def build_guardians_talk_schedule_end(
      talk: str,
      location: str,
      schedule_end_date: str ) -> GuardiansTalkScheduleEndInput:
   return GuardiansTalkScheduleEndInput(
      talk_name=talk,
      location=location,
      schedule_end_date=schedule_end_date )
