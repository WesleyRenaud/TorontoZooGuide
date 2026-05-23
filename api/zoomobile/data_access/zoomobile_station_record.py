from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate


@dataclass( frozen=True )
class ZoomobileStationRecord:
   name: str
   on_winter_route: bool
   description: str
   x_coord: Coordinate
   y_coord: Coordinate
