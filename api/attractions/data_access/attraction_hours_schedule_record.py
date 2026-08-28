from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class AttractionHoursScheduleRecord:
   attraction: str
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   weekday_start_time: Types.ScheduleTimeKey
   weekday_end_time: Types.ScheduleTimeKey
   weekend_holiday_start_time: Types.ScheduleTimeKey
   weekend_holiday_end_time: Types.ScheduleTimeKey
