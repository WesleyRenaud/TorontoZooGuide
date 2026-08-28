from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class GuardiansTalkScheduleRecord:
   name: str
   location: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   maximum_duration: int | None
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   talk_time: Types.ScheduleTimeKey
