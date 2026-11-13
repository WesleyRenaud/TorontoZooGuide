from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalVisibilitySchedule:
   species: str
   exhibit: str
   start_date: str | None
   end_date: str | None
   daily_start_time: str
   daily_end_time: str
   message: str
