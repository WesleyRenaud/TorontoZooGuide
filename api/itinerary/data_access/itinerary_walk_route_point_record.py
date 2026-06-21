from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryWalkRoutePointRecord:
   point_sequence: int
   walk_node_id: str
   x: float
   y: float
   x_px: float
   y_px: float
