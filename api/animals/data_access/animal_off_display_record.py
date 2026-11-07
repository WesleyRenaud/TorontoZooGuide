from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class AnimalOffDisplayRecord:
   species: str
   is_off_display: bool
   start: Types.DateKey | None
   end: Types.DateKey | None
   off_for_season: bool
