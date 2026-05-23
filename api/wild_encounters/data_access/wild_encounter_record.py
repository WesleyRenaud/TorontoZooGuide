from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate


@dataclass( frozen=True )
class WildEncounterRecord:
   name: str
   meeting_spot: str
   link: str | None
   maximum_duration: int | None
   x_coord: Coordinate
   y_coord: Coordinate
