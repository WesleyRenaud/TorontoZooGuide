from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class WildEncounterScheduleRecord:
   name: str
   meeting_spot: str
   link: str | None
   maximum_duration: int | None
   x_coord: Coordinate
   y_coord: Coordinate
   schedule_start_date: DateKey
   schedule_end_date: DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   encounter_time: ScheduleTimeKey
   is_cancelled: bool
