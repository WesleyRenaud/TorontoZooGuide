from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class WildEncounterRecord:
   name: str
   meeting_spot: str
   link: str | None
   maximum_duration: int | None
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   region: str
