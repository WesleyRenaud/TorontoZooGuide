from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class GuardiansTalkScheduleInput:
   talk_name: str
   location: str
   start_date: str
   end_date: DateKey | None
   monday_time: ScheduleTimeKey
   tuesday_time: ScheduleTimeKey
   wednesday_time: ScheduleTimeKey
   thursday_time: ScheduleTimeKey
   friday_time: ScheduleTimeKey
   saturday_time: ScheduleTimeKey
   sunday_time: ScheduleTimeKey
   message: str
