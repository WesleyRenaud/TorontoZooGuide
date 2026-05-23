from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate


@dataclass( frozen=True )
class MeetTheGuardiansTalkRecord:
   name: str
   location: str
   x_coord: Coordinate
   y_coord: Coordinate
   maximum_duration: int | None
