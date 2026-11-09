from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class RecordedOpeningSchedule:
   name: str
   start_date: str
   end_date: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   message: str
