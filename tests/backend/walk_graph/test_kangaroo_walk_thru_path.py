from __future__ import annotations

from collections import defaultdict

from api.walk_graph.data_access.load_map_location_walk_nodes import load_map_location_walk_nodes
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from api.walk_graph.shortest_path import build_walk_graph_adjacency
from api.walk_graph.shortest_path import shortest_path_distance
from api.walk_graph.shortest_path import shortest_path_node_ids
from api.walk_graph.shortest_path import WalkGraphAdjacency


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'


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


def test_kangaroo_walk_thru_attraction_pins_mid_one_way_path() -> None:
   graph = load_walk_graph()
   adjacency = build_walk_graph_adjacency( graph )
   one_way_successors = _one_way_successors( adjacency )

   attraction_walk_node = walk_node_for_map_location(
      MapLocationKind.ATTRACTION,
      KANGAROO_WALK_THRU )
   assert attraction_walk_node is not None

   attraction_node_id = attraction_walk_node.walk_node_id
   walk_node_row = next(
      row
      for row in load_map_location_walk_nodes()
      if row.kind == MapLocationKind.ATTRACTION and row.name == KANGAROO_WALK_THRU
   )
   assert walk_node_row.walk_node_id == attraction_node_id

   chain = _unique_one_way_path_through( one_way_successors, attraction_node_id )
   entry_node_id = chain[ 0 ]
   exit_node_id = chain[ -1 ]
   attraction_index = chain.index( attraction_node_id )

   assert 0 < attraction_index < len( chain ) - 1

   for from_id, to_id in zip( chain, chain[ 1 : ] ):
      assert to_id in one_way_successors.get( from_id, [] )
      assert from_id not in one_way_successors.get( to_id, [] )

   path_to_attraction = shortest_path_node_ids(
      graph,
      entry_node_id,
      attraction_node_id )
   assert path_to_attraction == chain[ : attraction_index + 1 ]

   path_from_attraction_to_entry = shortest_path_node_ids(
      graph,
      attraction_node_id,
      entry_node_id )
   assert path_from_attraction_to_entry is not None
   assert exit_node_id in path_from_attraction_to_entry
   assert path_from_attraction_to_entry[ 1 ] == chain[ attraction_index + 1 ]

   assert shortest_path_distance(
      graph,
      entry_node_id,
      attraction_node_id ) < shortest_path_distance(
         graph,
         exit_node_id,
         attraction_node_id )
