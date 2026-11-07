from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalDaySeasonalViewabilityRecord:
   species: str
   exhibit: str
   month: int
   day: int
   value: float
