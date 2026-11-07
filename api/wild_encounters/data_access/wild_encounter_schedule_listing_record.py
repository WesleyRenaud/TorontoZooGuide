from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class WildEncounterScheduleListingRecord:
   wild_encounter: str
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   encounter_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
