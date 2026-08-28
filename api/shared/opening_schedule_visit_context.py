from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ..types import Types


@dataclass( frozen=True )
class OpeningScheduleVisitContext:
   normalized_month: int
   normalized_day: int
   target_date: date
   weekday: int
   is_weekend_or_holiday: bool
