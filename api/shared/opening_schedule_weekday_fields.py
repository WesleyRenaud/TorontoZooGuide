from __future__ import annotations

from dataclasses import dataclass

from ..types import Types


@dataclass( frozen=True )
class OpeningScheduleWeekdayFields:
   start_date: Types.DateKey
   end_date: Types.DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   message: str | None
