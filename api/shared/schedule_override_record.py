from __future__ import annotations

from typing import Protocol


class ScheduleOverrideRecord( Protocol ):
   override_start_date: str
   override_end_date: str | None
   is_closed: bool
   override_message: str | None
