from __future__ import annotations

from functools import lru_cache

from .data_access.map_location_walk_node_provider import MapLocationWalkNodeProvider
from .domain.map_location_key import MapLocationKey
from .domain.map_location_kind import MapLocationKind
from .domain.map_location_walk_node import MapLocationWalkNode


class MapLocationWalkNodeLookup():
   @classmethod
   @lru_cache( maxsize=1 )
   def by_key( cls ) -> dict[
         MapLocationKey,
         MapLocationWalkNode,
      ]:
      return {
         row.location_key(): row
         for row in MapLocationWalkNodeProvider.fetch_records()
      }


   @classmethod
   def for_map_location(
         cls,
         kind: MapLocationKind,
         name: str,
         *,
         location: str = '' ) -> MapLocationWalkNode | None:
      return cls.by_key().get(
         MapLocationKey.for_kind( kind, name, location=location ) )
