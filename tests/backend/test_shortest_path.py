from __future__ import annotations

import pytest

from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator


def test_shortest_path_distance_from_node_to_itself_is_zero() -> None:
   graph = load_walk_graph()

   assert ShortestPathCalculator.distance(
      graph,
      graph[ 'entrance_node_id' ],
      graph[ 'entrance_node_id' ] ) == 0.0


def test_shortest_path_distances_are_symmetric_for_known_nodes() -> None:
   graph = load_walk_graph()
   entrance_id = graph[ 'entrance_node_id' ]
   sample_node_id = graph[ 'nodes' ][ 0 ][ 'id' ]

   forward = ShortestPathCalculator.distance( graph, entrance_id, sample_node_id )
   reverse = ShortestPathCalculator.distance( graph, sample_node_id, entrance_id )

   assert forward is not None
   assert reverse == pytest.approx( forward )


def test_shortest_path_includes_length_matching_distance() -> None:
   graph = load_walk_graph()
   entrance_id = graph[ 'entrance_node_id' ]
   neighbor_id = graph[ 'edges' ][ 0 ][ 'from' ]

   if neighbor_id != entrance_id:
      target_id = neighbor_id
   else:
      target_id = graph[ 'edges' ][ 0 ][ 'to' ]

   path = ShortestPathCalculator.find( graph, entrance_id, target_id )

   assert path is not None
   assert path.node_ids[ 0 ] == entrance_id
   assert path.node_ids[ -1 ] == target_id
   assert path.length_px == ShortestPathCalculator.distances( graph, entrance_id )[ target_id ]
   assert ShortestPathCalculator.node_ids( graph, entrance_id, target_id ) == path.node_ids
