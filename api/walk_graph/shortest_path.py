from __future__ import annotations

from collections import defaultdict
import heapq

from .domain.walk_graph import WalkGraph


WalkGraphAdjacency = dict[ str, list[ tuple[ str, float ] ] ]


def build_walk_graph_adjacency( graph: WalkGraph ) -> WalkGraphAdjacency:
   adjacency: WalkGraphAdjacency = defaultdict( list )

   for edge in graph[ 'edges' ]:
      from_id = str( edge[ 'from' ] )
      to_id = str( edge[ 'to' ] )
      length_px = float( edge[ 'length_px' ] )

      adjacency[ from_id ].append( ( to_id, length_px ) )
      adjacency[ to_id ].append( ( from_id, length_px ) )

   return dict( adjacency )


def shortest_path_distances(
      graph: WalkGraph,
      start_node_id: str,
      *,
      adjacency: WalkGraphAdjacency | None = None ) -> dict[ str, float ]:
   if adjacency is None:
      adjacency = build_walk_graph_adjacency( graph )
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


def shortest_path_distance(
      graph: WalkGraph,
      from_node_id: str,
      to_node_id: str ) -> float | None:
   if from_node_id == to_node_id:
      return 0.0

   return shortest_path_distances( graph, from_node_id ).get( to_node_id )


def shortest_path_node_ids(
      graph: WalkGraph,
      from_node_id: str,
      to_node_id: str ) -> list[ str ] | None:
   if from_node_id == to_node_id:
      return [ from_node_id ]

   adjacency = build_walk_graph_adjacency( graph )
   distances: dict[ str, float ] = { from_node_id: 0.0 }
   previous: dict[ str, str ] = {}
   queue: list[ tuple[ float, str ] ] = [ ( 0.0, from_node_id ) ]

   while queue:
      distance, node_id = heapq.heappop( queue )

      if node_id == to_node_id:
         path = [ to_node_id ]

         while path[ -1 ] != from_node_id:
            path.append( previous[ path[ -1 ] ] )

         path.reverse()
         return path

      if distance > distances[ node_id ]:
         continue

      for neighbor_id, edge_length_px in adjacency.get( node_id, [] ):
         next_distance = distance + edge_length_px

         if (
               neighbor_id not in distances
               or next_distance < distances[ neighbor_id ] ):
            distances[ neighbor_id ] = next_distance
            previous[ neighbor_id ] = node_id
            heapq.heappush( queue, ( next_distance, neighbor_id ) )

   return None
