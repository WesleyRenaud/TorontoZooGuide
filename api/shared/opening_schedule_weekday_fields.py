from __future__ import annotations

from dataclasses import dataclass

from ..types import DateKey


@dataclass( frozen=True )
class OpeningScheduleWeekdayFields:
   start_date: DateKey
   end_date: DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   message: str | None
