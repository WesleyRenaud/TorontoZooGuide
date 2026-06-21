from __future__ import annotations

from .domain.walk_graph import WalkGraph
from .shortest_path import shortest_path_distances


def representative_walk_node_id_from_candidates(
      graph: WalkGraph,
      from_node_id: str,
      candidate_node_ids: tuple[ str, ... ] ) -> str | None:
   if not candidate_node_ids:
      return None

   if len( candidate_node_ids ) == 1:
      return candidate_node_ids[ 0 ]

   distances = shortest_path_distances( graph, from_node_id )

   return _closest_walk_node_from_distances(
      distances,
      candidate_node_ids )


def _closest_walk_node_from_distances(
      distances: dict[ str, float ],
      candidate_node_ids: tuple[ str, ... ] ) -> str | None:
   walk_node_id: str | None = None
   shortest_distance_px: float | None = None

   for node_id in candidate_node_ids:
      distance_px = distances.get( node_id )

      if distance_px is None:
         continue

      if (
            shortest_distance_px is None
            or distance_px < shortest_distance_px ):
         shortest_distance_px = distance_px
         walk_node_id = node_id

   return walk_node_id
