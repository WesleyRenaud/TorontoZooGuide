from __future__ import annotations

from typing import Protocol


class OpeningScheduleRecord( Protocol ):
   schedule_start_date: str
   schedule_end_date: str | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   schedule_message: str | None
