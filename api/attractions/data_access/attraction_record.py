from __future__ import annotations

from dataclasses import dataclass, field

from ...shared.peak_months import PeakMonths
from ...types import Types


@dataclass( frozen=True )
class AttractionRecord:
   name: str
   free_with_admission: bool
   description: str
   info_link: str
   hyperlink_text: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   region: str
   peak_months: PeakMonths = field( default_factory=PeakMonths )
   weekday_start_time: Types.ScheduleTimeKey = None
   weekday_end_time: Types.ScheduleTimeKey = None
   weekend_holiday_start_time: Types.ScheduleTimeKey = None
   weekend_holiday_end_time: Types.ScheduleTimeKey = None
   is_also_transportation: bool = False
