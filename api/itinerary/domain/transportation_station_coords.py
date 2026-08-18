from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate


@dataclass( frozen=True )
class TransportationStationCoords:
   name: str | None = None
   x_coord: Coordinate | None = None
   y_coord: Coordinate | None = None
