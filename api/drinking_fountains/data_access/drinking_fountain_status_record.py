from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class DrinkingFountainStatusRecord:
   is_closed: bool
   start_date: Types.DateKey
   end_date: Types.DateKey | None
   closed_message: str | None
