from __future__ import annotations

import heapq

from .domain.walk_graph import WalkGraph
from .shortest_path import ShortestPath
from .shortest_path import WalkGraphAdjacency
from .walk_graph_adjacency_builder import WalkGraphAdjacencyBuilder


class ShortestPathCalculator():
   @classmethod
   def distances(
         cls,
         graph: WalkGraph,
         start_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> dict[ str, float ]:
      if adjacency is None:
         adjacency = WalkGraphAdjacencyBuilder.build( graph )
      distances: dict[ str, float ] = { start_node_id: 0.0 }
      queue: list[ tuple[ float, str ] ] = [ ( 0.0, start_node_id ) ]

      while queue:
         distance, node_id = heapq.heappop( queue )

         if distance > distances[ node_id ]:
            continue

         for neighbor_id, edge_length_px in adjacency.get( node_id, [] ):
            next_distance = distance + edge_length_px

            if (
                  neighbor_id not in distances
                  or next_distance < distances[ neighbor_id ] ):
               distances[ neighbor_id ] = next_distance
               heapq.heappush( queue, ( next_distance, neighbor_id ) )

      return distances


   @classmethod
   def distance(
         cls,
         graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> float | None:
      if from_node_id == to_node_id:
         return 0.0

      return cls.distances(
         graph,
         from_node_id,
         adjacency=adjacency ).get( to_node_id )


   @classmethod
   def find(
         cls,
         graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> ShortestPath | None:
      if from_node_id == to_node_id:
         return ShortestPath( node_ids=[ from_node_id ], length_px=0.0 )

      if adjacency is None:
         adjacency = WalkGraphAdjacencyBuilder.build( graph )

      distances: dict[ str, float ] = { from_node_id: 0.0 }
      previous: dict[ str, str ] = {}
      queue: list[ tuple[ float, str ] ] = [ ( 0.0, from_node_id ) ]

      while queue:
         distance, node_id = heapq.heappop( queue )

         if distance > distances[ node_id ]:
            continue

         if node_id == to_node_id:
            path = [ to_node_id ]

            while path[ -1 ] != from_node_id:
               path.append( previous[ path[ -1 ] ] )

            path.reverse()
            return ShortestPath( node_ids=path, length_px=distance )

         for neighbor_id, edge_length_px in adjacency.get( node_id, [] ):
            next_distance = distance + edge_length_px

            if (
                  neighbor_id not in distances
                  or next_distance < distances[ neighbor_id ] ):
               distances[ neighbor_id ] = next_distance
               previous[ neighbor_id ] = node_id
               heapq.heappush( queue, ( next_distance, neighbor_id ) )

      return None


   @classmethod
   def node_ids(
         cls,
         graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> list[ str ] | None:
      path = cls.find(
         graph,
         from_node_id,
         to_node_id,
         adjacency=adjacency )

      if path is None:
         return None

      return path.node_ids
