from __future__ import annotations

from typing import TypedDict

from .walk_graph_landmark import WalkGraphLandmark
from .walk_graph_node import WalkGraphNode


class WalkGraph( TypedDict ):
   map_width_px: int
   map_height_px: int
   entrance_node_id: str
   entrance_landmark: WalkGraphLandmark
   nodes: list[ WalkGraphNode ]
   edges: list[ dict[ str, object ] ]
