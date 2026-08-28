from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class MeetTheGuardiansTalkRecord:
   name: str
   location: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   maximum_duration: int | None
