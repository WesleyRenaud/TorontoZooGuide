from __future__ import annotations

import pytest

from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path import shortest_path_distance
from api.walk_graph.shortest_path import shortest_path_distances
from api.walk_graph.shortest_path import shortest_path_node_ids


def test_shortest_path_distance_from_node_to_itself_is_zero() -> None:
   graph = load_walk_graph()

   assert shortest_path_distance(
      graph,
      graph[ 'entrance_node_id' ],
      graph[ 'entrance_node_id' ] ) == 0.0


def test_shortest_path_distances_are_symmetric_for_known_nodes() -> None:
   graph = load_walk_graph()
   entrance_id = graph[ 'entrance_node_id' ]
   sample_node_id = graph[ 'nodes' ][ 0 ][ 'id' ]

   forward = shortest_path_distance( graph, entrance_id, sample_node_id )
   reverse = shortest_path_distance( graph, sample_node_id, entrance_id )

   assert forward is not None
   assert reverse == pytest.approx( forward )


def test_shortest_path_node_ids_connects_entrance_to_neighbor() -> None:
   graph = load_walk_graph()
   entrance_id = graph[ 'entrance_node_id' ]
   neighbor_id = graph[ 'edges' ][ 0 ][ 'from' ]

   if neighbor_id != entrance_id:
      target_id = neighbor_id
   else:
      target_id = graph[ 'edges' ][ 0 ][ 'to' ]

   path = shortest_path_node_ids( graph, entrance_id, target_id )

   assert path is not None
   assert path[ 0 ] == entrance_id
   assert path[ -1 ] == target_id
   assert shortest_path_distances( graph, entrance_id )[ target_id ] > 0
