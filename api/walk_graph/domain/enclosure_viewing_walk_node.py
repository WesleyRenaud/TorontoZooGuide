from __future__ import annotations

from typing import TypedDict


class EnclosureViewingWalkNode( TypedDict ):
   species: str
   exhibit: str
   enclosure_type: str
   x: float
   y: float
   walk_node_id: str
   snap_distance_px: float
