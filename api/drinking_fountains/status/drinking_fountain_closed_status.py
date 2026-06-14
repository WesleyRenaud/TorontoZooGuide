from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class DrinkingFountainClosedStatus:
   start_date: DateKey
   end_date: DateKey | None
   message: str
