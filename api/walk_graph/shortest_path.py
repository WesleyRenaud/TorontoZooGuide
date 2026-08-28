from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ShortestPath:
   node_ids: list[ str ]
   length_px: float


WalkGraphAdjacency = dict[ str, list[ tuple[ str, float ] ] ]
