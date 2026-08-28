from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class AttractionHoursTimeBounds:
   open_time: Types.ScheduleTimeKey
   close_time: Types.ScheduleTimeKey
   operating_date: Types.DateKey
