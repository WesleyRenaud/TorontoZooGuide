from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class TransportationRecord:
   name: str
   is_also_attraction: bool
   free_with_admission: bool
   description: str
   info_link: str
   hyperlink_text: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   region: str
   weekday_start_time: Types.ScheduleTimeKey
   weekday_end_time: Types.ScheduleTimeKey
   weekend_holiday_start_time: Types.ScheduleTimeKey
   weekend_holiday_end_time: Types.ScheduleTimeKey
