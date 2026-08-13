from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, ScheduleTimeKey, SeasonalMultiplier


@dataclass( frozen=True )
class AttractionRecord:
   name: str
   free_with_admission: bool
   description: str
   info_link: str
   hyperlink_text: str
   x_coord: Coordinate
   y_coord: Coordinate
   region: str
   weekday_multiplier: SeasonalMultiplier
   weekend_holiday_multiplier: SeasonalMultiplier
   weekday_start_time: ScheduleTimeKey = None
   weekday_end_time: ScheduleTimeKey = None
   weekend_holiday_start_time: ScheduleTimeKey = None
   weekend_holiday_end_time: ScheduleTimeKey = None
   is_also_transportation: bool = False
