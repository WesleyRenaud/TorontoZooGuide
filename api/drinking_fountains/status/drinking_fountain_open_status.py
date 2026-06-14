from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class DrinkingFountainOpenStatus:
   start_date: DateKey
   end_date: DateKey | None
