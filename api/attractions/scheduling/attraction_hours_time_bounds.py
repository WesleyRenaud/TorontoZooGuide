from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class AttractionHoursTimeBounds:
   open_time: ScheduleTimeKey
   close_time: ScheduleTimeKey
   operating_date: DateKey
