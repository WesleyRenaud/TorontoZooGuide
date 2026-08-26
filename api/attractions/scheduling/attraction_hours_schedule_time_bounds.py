from __future__ import annotations

from dataclasses import dataclass

from .attraction_hours_time_bounds import AttractionHoursTimeBounds


@dataclass( frozen=True )
class AttractionHoursScheduleTimeBounds:
   weekday: AttractionHoursTimeBounds
   weekend_holiday: AttractionHoursTimeBounds
