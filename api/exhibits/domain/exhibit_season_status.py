from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ExhibitSeasonStatus():
   exhibit: str
   is_closed: bool
   start: date | None
   end: date | None
   closed_for_season: bool
