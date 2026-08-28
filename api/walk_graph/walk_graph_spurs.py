from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache

from .domain.walk_graph import WalkGraph
from .shortest_path import WalkGraphAdjacency
from .walk_graph_adjacency_builder import WalkGraphAdjacencyBuilder


MIN_SPUR_NODE_COUNT = 15
MAX_SPUR_NODE_FRACTION = 0.2
SPUR_ATTACHMENT_ACTIVATION_RADIUS_PX = 100.0


@dataclass( frozen=True )
class WalkGraphSpur:
   node_ids: frozenset[ str ]
   attachment_node_ids: frozenset[ str ]


def walk_graph_spur_index_for_viewing_node_ids(
      spurs: list[ WalkGraphSpur ],
      viewing_node_ids: list[ str ] ) -> int | None:
   best_index: int | None = None
   best_overlap = 0

   for index, spur in enumerate( spurs ):
      overlap = sum(
         1
         for node_id in viewing_node_ids
         if node_id in spur.node_ids
      )

      if overlap > best_overlap:
         best_overlap = overlap
         best_index = index

   if best_overlap == 0:
      return None

   return best_index


def is_walk_graph_spur_active(
      spur: WalkGraphSpur,
      current_node_id: str,
      distances_from_current: dict[ str, float ] ) -> bool:
   if current_node_id in spur.node_ids:
      return True

   return any(
      distances_from_current.get( attachment_node_id, float( 'inf' ) )
         <= SPUR_ATTACHMENT_ACTIVATION_RADIUS_PX
      for attachment_node_id in spur.attachment_node_ids
   )


@lru_cache( maxsize=1 )
def walk_graph_spurs() -> list[ WalkGraphSpur ]:
   from .data_access.load_walk_graph import load_walk_graph

   return walk_graph_spurs_for_graph( load_walk_graph() )


def walk_graph_spurs_for_graph( graph: WalkGraph ) -> list[ WalkGraphSpur ]:
   return _walk_graph_spurs_from_graph( graph )


def _walk_graph_spurs_from_graph( graph: WalkGraph ) -> list[ WalkGraphSpur ]:
   adjacency = WalkGraphAdjacencyBuilder.build( graph )
   entrance_node_id = str( graph[ 'entrance_node_id' ] )
   max_spur_node_count = int( len( adjacency ) * MAX_SPUR_NODE_FRACTION )
   spur_regions: list[ WalkGraphSpur ] = []

   for bridge in _find_walk_graph_bridges( adjacency ):
      for attachment_node_id, spur_node_ids in _walk_graph_spur_sides_for_bridge(
            bridge,
            adjacency,
            entrance_node_id=entrance_node_id,
            max_spur_node_count=max_spur_node_count ):

         if len( spur_node_ids ) < MIN_SPUR_NODE_COUNT:
            continue

         _append_walk_graph_spur_region(
            spur_regions,
            spur_node_ids=spur_node_ids,
            attachment_node_id=attachment_node_id )

   return _merge_subset_walk_graph_spurs( spur_regions )


def _append_walk_graph_spur_region(
      spur_regions: list[ WalkGraphSpur ],
      *,
      spur_node_ids: set[ str ],
      attachment_node_id: str ) -> None:
   spur_node_key = frozenset( spur_node_ids )

   for index, spur_region in enumerate( spur_regions ):
      if spur_region.node_ids != spur_node_key:
         continue

      spur_regions[ index ] = WalkGraphSpur(
         node_ids=spur_region.node_ids,
         attachment_node_ids=spur_region.attachment_node_ids | {
            attachment_node_id,
         } )
      return

   spur_regions.append(
      WalkGraphSpur(
         node_ids=spur_node_key,
         attachment_node_ids=frozenset( { attachment_node_id } ) ) )


def _merge_subset_walk_graph_spurs(
      spur_regions: list[ WalkGraphSpur ] ) -> list[ WalkGraphSpur ]:
   ordered_regions = sorted(
      spur_regions,
      key=lambda spur_region: len( spur_region.node_ids ),
      reverse=True )
   merged_regions: list[ WalkGraphSpur ] = []

   for spur_region in ordered_regions:
      if any(
            spur_region.node_ids <= merged_region.node_ids
            for merged_region in merged_regions ):
         continue

      merged_regions = [
         merged_region
         for merged_region in merged_regions
         if not merged_region.node_ids <= spur_region.node_ids
      ]
      merged_regions.append( spur_region )

   return merged_regions


def _walk_graph_spur_sides_for_bridge(
      bridge: tuple[ str, str ],
      adjacency: WalkGraphAdjacency,
      *,
      entrance_node_id: str,
      max_spur_node_count: int ) -> list[ tuple[ str, set[ str ] ] ]:
   from_node_id, to_node_id = bridge
   sides: list[ tuple[ str, set[ str ] ] ] = []

   for attachment_node_id, other_node_id in (
         ( from_node_id, to_node_id ),
         ( to_node_id, from_node_id ),
   ):
      main_component = _walk_graph_component_without_edge(
         attachment_node_id,
         bridge,
         adjacency )
      spur_component = _walk_graph_component_without_edge(
         other_node_id,
         bridge,
         adjacency )

      if entrance_node_id not in main_component:
         continue

      if len( main_component ) < len( spur_component ):
         continue

      if len( spur_component ) > max_spur_node_count:
         continue

      sides.append( ( attachment_node_id, spur_component ) )

   return sides


def _walk_graph_component_without_edge(
      start_node_id: str,
      bridge: tuple[ str, str ],
      adjacency: WalkGraphAdjacency ) -> set[ str ]:
   blocked_edge = frozenset( bridge )
   visited = { start_node_id }
   queue = deque( [ start_node_id ] )

   while queue:
      node_id = queue.popleft()

      for neighbor_id, _edge_length_px in adjacency.get( node_id, [] ):
         if neighbor_id in visited:
            continue

         if frozenset( ( node_id, neighbor_id ) ) == blocked_edge:
            continue

         visited.add( neighbor_id )
         queue.append( neighbor_id )

   return visited


def _find_walk_graph_bridges(
      adjacency: WalkGraphAdjacency ) -> list[ tuple[ str, str ] ]:
   bridges: list[ tuple[ str, str ] ] = []
   visited: set[ str ] = set()
   discovery_order: dict[ str, int ] = {}
   low_link: dict[ str, int ] = {}
   parent: dict[ str, str | None ] = {}
   timer = 0

   def visit( node_id: str ) -> None:
      nonlocal timer
      visited.add( node_id )
      discovery_order[ node_id ] = timer
      low_link[ node_id ] = timer
      timer += 1

      for neighbor_id, _edge_length_px in adjacency.get( node_id, [] ):
         if neighbor_id not in visited:
            parent[ neighbor_id ] = node_id
            visit( neighbor_id )
            low_link[ node_id ] = min(
               low_link[ node_id ],
               low_link[ neighbor_id ] )

            if low_link[ neighbor_id ] > discovery_order[ node_id ]:
               bridges.append( ( node_id, neighbor_id ) )

            continue

         if neighbor_id != parent.get( node_id ):
            low_link[ node_id ] = min(
               low_link[ node_id ],
               discovery_order[ neighbor_id ] )

   for node_id in adjacency:
      if node_id not in visited:
         parent[ node_id ] = None
         visit( node_id )

   return bridges
