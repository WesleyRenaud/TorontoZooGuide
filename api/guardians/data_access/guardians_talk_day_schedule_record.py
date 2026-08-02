from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, ScheduleTimeKey


@dataclass( frozen=True )
class GuardiansTalkDayScheduleRecord:
   name: str
   location: str
   x_coord: Coordinate
   y_coord: Coordinate
   maximum_duration: int | None
   talk_time: ScheduleTimeKey
