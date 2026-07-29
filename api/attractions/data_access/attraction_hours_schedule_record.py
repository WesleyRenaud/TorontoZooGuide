from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class AttractionHoursScheduleRecord:
   attraction: str
   schedule_start_date: DateKey
   schedule_end_date: DateKey | None
   weekday_start_time: ScheduleTimeKey
   weekday_end_time: ScheduleTimeKey
   weekend_holiday_start_time: ScheduleTimeKey
   weekend_holiday_end_time: ScheduleTimeKey
