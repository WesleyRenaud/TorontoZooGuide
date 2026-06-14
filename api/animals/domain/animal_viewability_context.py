from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class AnimalViewabilityContext:
   calendar_month: int
   day_of_month: int
   target_date: date
   temp: float
   sigma: int
