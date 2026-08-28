from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class RestaurantScheduleRecord:
   restaurant: str
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   schedule_message: str | None
