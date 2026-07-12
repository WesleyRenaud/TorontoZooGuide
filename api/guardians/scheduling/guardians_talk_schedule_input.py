from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class GuardiansTalkScheduleInput:
   talk_name: str
   location: str
   start_date: str
   end_date: DateKey | None
   talk_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str
