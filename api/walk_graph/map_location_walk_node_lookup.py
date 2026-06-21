from __future__ import annotations

from functools import lru_cache

from .data_access.load_map_location_walk_nodes import load_map_location_walk_nodes
from .domain.map_location_key import MapLocationKey
from .domain.map_location_kind import MapLocationKind
from .domain.map_location_walk_node import MapLocationWalkNode


@lru_cache( maxsize=1 )
def map_location_walk_nodes_by_key() -> dict[
      MapLocationKey,
      MapLocationWalkNode,
   ]:
   return {
      row.location_key(): row
      for row in load_map_location_walk_nodes()
   }


def walk_node_for_map_location(
      kind: MapLocationKind,
      name: str,
      *,
      location: str = '' ) -> MapLocationWalkNode | None:
   return map_location_walk_nodes_by_key().get(
      MapLocationKey.for_kind( kind, name, location=location ) )
