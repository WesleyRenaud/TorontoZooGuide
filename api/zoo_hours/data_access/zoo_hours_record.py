from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ZooHoursRecord:
   operating_date: DateKey
   early_admission_time: ScheduleTimeKey
   open_time: ScheduleTimeKey
   last_admission_time: ScheduleTimeKey
   close_time: ScheduleTimeKey
