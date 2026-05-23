from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class WildEncounterScheduleInput:
   wild_encounter: str
   start_date: str
   end_date: DateKey | None
   encounter_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str
