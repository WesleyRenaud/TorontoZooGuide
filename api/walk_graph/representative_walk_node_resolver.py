from __future__ import annotations

from .domain.walk_graph import WalkGraph
from .shortest_path_calculator import ShortestPathCalculator


class RepresentativeWalkNodeResolver():
   @classmethod
   def resolve(
         cls,
         graph: WalkGraph,
         from_node_id: str,
         candidate_node_ids: list[ str ] ) -> str | None:
      if not candidate_node_ids:
         return None

      if len( candidate_node_ids ) == 1:
         return candidate_node_ids[ 0 ]

      distances = ShortestPathCalculator.distances( graph, from_node_id )

      return cls._closest_from_distances(
         distances,
         candidate_node_ids )


   @classmethod
   def _closest_from_distances(
         cls,
         distances: dict[ str, float ],
         candidate_node_ids: list[ str ] ) -> str | None:
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
