from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class WildEncounterScheduleRecord:
   name: str
   meeting_spot: str
   link: str | None
   maximum_duration: int | None
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   region: str
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   encounter_time: Types.ScheduleTimeKey
   is_cancelled: bool
