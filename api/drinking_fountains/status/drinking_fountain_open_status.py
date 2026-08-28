from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class DrinkingFountainOpenStatus:
   start_date: Types.DateKey
   end_date: Types.DateKey | None
