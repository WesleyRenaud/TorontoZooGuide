from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class GuardiansTalkScheduleRecord:
   name: str
   location: str
   x_coord: Coordinate
   y_coord: Coordinate
   maximum_duration: int | None
   schedule_start_date: DateKey
   schedule_end_date: DateKey | None
   monday_time: ScheduleTimeKey
   tuesday_time: ScheduleTimeKey
   wednesday_time: ScheduleTimeKey
   thursday_time: ScheduleTimeKey
   friday_time: ScheduleTimeKey
   saturday_time: ScheduleTimeKey
   sunday_time: ScheduleTimeKey
