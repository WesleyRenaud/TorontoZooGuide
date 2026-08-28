from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class WildEncounterScheduleInput:
   wild_encounter: str
   start_date: str
   end_date: Types.DateKey | None
   encounter_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str
