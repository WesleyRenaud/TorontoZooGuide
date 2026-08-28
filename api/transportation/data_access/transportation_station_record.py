from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class TransportationStationRecord:
   name: str
   description: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
