from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, ScheduleTimeKey


@dataclass( frozen=True )
class TransportationRecord:
   name: str
   is_also_attraction: bool
   free_with_admission: bool
   description: str
   info_link: str
   hyperlink_text: str
   x_coord: Coordinate
   y_coord: Coordinate
   region: str
   weekday_start_time: ScheduleTimeKey
   weekday_end_time: ScheduleTimeKey
   weekend_holiday_start_time: ScheduleTimeKey
   weekend_holiday_end_time: ScheduleTimeKey
