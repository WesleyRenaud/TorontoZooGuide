from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class WildEncounterScheduleConflictRecord:
   wild_encounter: str
   encounter_time: ScheduleTimeKey
   schedule_start_date: DateKey
   schedule_end_date: DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str
