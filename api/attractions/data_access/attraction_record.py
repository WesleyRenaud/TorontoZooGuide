from __future__ import annotations

from dataclasses import dataclass

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
   weekday_multiplier: Types.SeasonalMultiplier
   weekend_holiday_multiplier: Types.SeasonalMultiplier
   weekday_start_time: Types.ScheduleTimeKey = None
   weekday_end_time: Types.ScheduleTimeKey = None
   weekend_holiday_start_time: Types.ScheduleTimeKey = None
   weekend_holiday_end_time: Types.ScheduleTimeKey = None
   is_also_transportation: bool = False
