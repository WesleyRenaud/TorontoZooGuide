from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class DrinkingFountainStatusRecord:
   is_closed: bool
   start_date: DateKey
   end_date: DateKey | None
   closed_message: str | None
