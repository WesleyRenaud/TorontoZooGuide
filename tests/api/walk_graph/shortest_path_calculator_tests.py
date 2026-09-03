from __future__ import annotations

import pytest

from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


BIDIRECTIONAL_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-1',
   'nodes': [
      _node( 'n-1', 0.0, 0.0 ),
      _node( 'n-2', 10.0, 0.0 ),
   ],
   'edges': [
      { 'from': 'n-1', 'to': 'n-2', 'length_px': 10.0 },
      { 'from': 'n-2', 'to': 'n-1', 'length_px': 10.0 },
   ],
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

STALE_QUEUE_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-1',
   'nodes': [
      _node( 'n-1', 0.0, 0.0 ),
      _node( 'n-2', 10.0, 0.0 ),
      _node( 'n-3', 20.0, 0.0 ),
   ],
   'edges': [
      { 'from': 'n-1', 'to': 'n-2', 'length_px': 10.0 },
      { 'from': 'n-1', 'to': 'n-3', 'length_px': 1.0 },
      { 'from': 'n-3', 'to': 'n-2', 'length_px': 1.0 },
   ],
}

STALE_INTERMEDIATE_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-1',
   'nodes': [
      _node( 'n-1', 0.0, 0.0 ),
      _node( 'n-2', 10.0, 0.0 ),
      _node( 'n-3', 20.0, 0.0 ),
      _node( 'n-4', 30.0, 0.0 ),
      _node( 'n-5', 40.0, 0.0 ),
   ],
   'edges': [
      { 'from': 'n-1', 'to': 'n-3', 'length_px': 10.0 },
      { 'from': 'n-1', 'to': 'n-2', 'length_px': 1.0 },
      { 'from': 'n-2', 'to': 'n-3', 'length_px': 1.0 },
      { 'from': 'n-3', 'to': 'n-4', 'length_px': 1.0 },
      { 'from': 'n-3', 'to': 'n-5', 'length_px': 50.0 },
   ],
}


def Test_Distance_TestSameNode_ExpectZero() -> None:
   assert ShortestPathCalculator.distance(
      BIDIRECTIONAL_GRAPH,
      'n-1',
      'n-1' ) == 0.0


def Test_Distance_TestKnownNodes_ExpectSymmetricDistance() -> None:
   forward = ShortestPathCalculator.distance( BIDIRECTIONAL_GRAPH, 'n-1', 'n-2' )
   reverse = ShortestPathCalculator.distance( BIDIRECTIONAL_GRAPH, 'n-2', 'n-1' )

   assert forward is not None
   assert reverse == pytest.approx( forward )


def Test_Find_TestSameNode_ExpectZeroLengthPath() -> None:
   path = ShortestPathCalculator.find(
      BIDIRECTIONAL_GRAPH,
      'n-1',
      'n-1' )

   assert path is not None
   assert path.node_ids == [ 'n-1' ]
   assert path.length_px == 0.0


def Test_Find_TestNeighborPath_ExpectLengthMatchesDistanceLookup() -> None:
   path = ShortestPathCalculator.find( BIDIRECTIONAL_GRAPH, 'n-1', 'n-2' )

   assert path is not None
   assert path.node_ids == [ 'n-1', 'n-2' ]
   assert path.length_px == ShortestPathCalculator.distances( BIDIRECTIONAL_GRAPH, 'n-1' )[ 'n-2' ]
   assert ShortestPathCalculator.node_ids( BIDIRECTIONAL_GRAPH, 'n-1', 'n-2' ) == path.node_ids


def Test_Find_TestOneWayChain_ExpectForwardPathAndNoReverseRoute() -> None:
   path_to_end = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-4' )
   path_to_middle = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-2' )
   reverse_path = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-2',
      'n-1' )

   assert path_to_end == [ 'n-1', 'n-2', 'n-3', 'n-4' ]
   assert path_to_middle == [ 'n-1', 'n-2' ]
   assert reverse_path is None
   assert ShortestPathCalculator.distance(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-2' ) < ShortestPathCalculator.distance(
         ONE_WAY_CHAIN_GRAPH,
         'n-1',
         'n-4' )


def Test_Distances_TestStaleQueueEntry_ExpectShortestDistance() -> None:
   assert ShortestPathCalculator.distances(
      STALE_QUEUE_GRAPH,
      'n-1' )[ 'n-2' ] == 2.0


def Test_Find_TestStaleQueueEntry_ExpectShortestPath() -> None:
   path = ShortestPathCalculator.find(
      STALE_QUEUE_GRAPH,
      'n-1',
      'n-2' )

   assert path is not None
   assert path.length_px == 2.0
   assert path.node_ids == [ 'n-1', 'n-3', 'n-2' ]


def Test_Find_TestStaleIntermediateNode_ExpectShortestPath() -> None:
   path = ShortestPathCalculator.find(
      STALE_INTERMEDIATE_GRAPH,
      'n-1',
      'n-5' )

   assert path is not None
   assert path.length_px == 52.0
   assert path.node_ids == [ 'n-1', 'n-2', 'n-3', 'n-5' ]
