from __future__ import annotations

from collections import defaultdict

from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.shortest_path import WalkGraphAdjacency
from api.walk_graph.walk_graph_adjacency_builder import WalkGraphAdjacencyBuilder


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


ONE_WAY_CHAIN_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-1',
   'nodes': [
      _node( 'n-1', 0.0, 0.0 ),
      _node( 'n-2', 10.0, 0.0 ),
      _node( 'n-3', 20.0, 0.0 ),
      _node( 'n-4', 30.0, 0.0 ),
   ],
   'edges': [
      { 'from': 'n-1', 'to': 'n-2', 'length_px': 10.0 },
      { 'from': 'n-2', 'to': 'n-3', 'length_px': 10.0 },
      { 'from': 'n-3', 'to': 'n-4', 'length_px': 10.0 },
   ],
}


def _one_way_successors( adjacency: WalkGraphAdjacency ) -> dict[ str, list[ str ] ]:
   successors: dict[ str, list[ str ] ] = defaultdict( list )

   for from_id, neighbors in adjacency.items():
      for to_id, _ in neighbors:
         if not any(
               neighbor_id == from_id
               for neighbor_id, _ in adjacency.get( to_id, [] ) ):
            successors[ from_id ].append( to_id )

   return dict( successors )


def _unique_one_way_path_through(
      one_way_successors: dict[ str, list[ str ] ],
      node_id: str ) -> list[ str ]:
   predecessors = {
      to_id: from_id
      for from_id, to_ids in one_way_successors.items()
      for to_id in to_ids
   }

   start = node_id

   while start in predecessors:
      start = predecessors[ start ]

   path = [ start ]

   while path[ -1 ] in one_way_successors:
      next_ids = one_way_successors[ path[ -1 ] ]

      if len( next_ids ) != 1:
         break

      path.append( next_ids[ 0 ] )

   assert node_id in path
   return path


def Test_Build_TestDirectedEdges_ExpectAdjacencyLists() -> None:
   adjacency = WalkGraphAdjacencyBuilder.build( ONE_WAY_CHAIN_GRAPH )

   assert adjacency[ 'n-1' ] == [ ( 'n-2', 10.0 ) ]
   assert adjacency[ 'n-2' ] == [ ( 'n-3', 10.0 ) ]
   assert adjacency[ 'n-3' ] == [ ( 'n-4', 10.0 ) ]
   assert 'n-4' not in adjacency


def Test_Build_TestOneWayChain_ExpectUniquePathThroughMiddleNode() -> None:
   adjacency = WalkGraphAdjacencyBuilder.build( ONE_WAY_CHAIN_GRAPH )
   one_way_successors = _one_way_successors( adjacency )
   middle_node_id = 'n-2'
   chain = _unique_one_way_path_through( one_way_successors, middle_node_id )
   middle_index = chain.index( middle_node_id )

   assert chain == [ 'n-1', 'n-2', 'n-3', 'n-4' ]
   assert 0 < middle_index < len( chain ) - 1

   for from_id, to_id in zip( chain, chain[ 1 : ] ):
      assert to_id in one_way_successors.get( from_id, [] )
      assert from_id not in one_way_successors.get( to_id, [] )
