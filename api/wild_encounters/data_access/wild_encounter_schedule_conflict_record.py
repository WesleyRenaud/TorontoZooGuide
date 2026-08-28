from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class WildEncounterScheduleConflictRecord:
   wild_encounter: str
   encounter_time: Types.ScheduleTimeKey
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str
