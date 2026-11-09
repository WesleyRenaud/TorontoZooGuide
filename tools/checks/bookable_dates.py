from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .week_schedule import WeekSchedule


@dataclass( frozen=True )
class BookableDates:
   dates: list[ date ]
   failure: str | None
   schedule: WeekSchedule | None = None
