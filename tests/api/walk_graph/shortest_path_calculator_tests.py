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
   result = ShortestPathCalculator.distance(
      BIDIRECTIONAL_GRAPH,
      'n-1',
      'n-1' )

   assert result == 0.0


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
   start_node_id = 'n-1'
   end_node_id = 'n-2'
   distances = ShortestPathCalculator.distances( BIDIRECTIONAL_GRAPH, start_node_id )

   path = ShortestPathCalculator.find( BIDIRECTIONAL_GRAPH, start_node_id, end_node_id )

   assert path is not None
   assert path.node_ids == [ start_node_id, end_node_id ]
   assert path.length_px == distances[ end_node_id ]


def Test_NodeIds_TestNeighborPath_ExpectSameNodesAsFind() -> None:
   start_node_id = 'n-1'
   end_node_id = 'n-2'
   path = ShortestPathCalculator.find( BIDIRECTIONAL_GRAPH, start_node_id, end_node_id )

   node_ids = ShortestPathCalculator.node_ids(
      BIDIRECTIONAL_GRAPH,
      start_node_id,
      end_node_id )

   assert node_ids == path.node_ids


def Test_NodeIds_TestOneWayChain_ExpectForwardPath() -> None:
   node_ids = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-4' )

   assert node_ids == [ 'n-1', 'n-2', 'n-3', 'n-4' ]


def Test_NodeIds_TestOneWayChainMiddle_ExpectPartialPath() -> None:
   node_ids = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-2' )

   assert node_ids == [ 'n-1', 'n-2' ]


def Test_NodeIds_TestOneWayChainReverse_ExpectNone() -> None:
   node_ids = ShortestPathCalculator.node_ids(
      ONE_WAY_CHAIN_GRAPH,
      'n-2',
      'n-1' )

   assert node_ids is None


def Test_Distance_TestOneWayChain_ExpectShorterThanFullPath() -> None:
   near_distance = ShortestPathCalculator.distance(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-2' )
   far_distance = ShortestPathCalculator.distance(
      ONE_WAY_CHAIN_GRAPH,
      'n-1',
      'n-4' )

   assert near_distance < far_distance


def Test_Distances_TestStaleQueueEntry_ExpectShortestDistance() -> None:
   start_node_id = 'n-1'
   end_node_id = 'n-2'
   short_edge = 1.0
   expected_distance = short_edge + short_edge

   distances = ShortestPathCalculator.distances( STALE_QUEUE_GRAPH, start_node_id )

   assert distances[ end_node_id ] == expected_distance


def Test_Find_TestStaleQueueEntry_ExpectShortestPath() -> None:
   start_node_id = 'n-1'
   via_node_id = 'n-3'
   end_node_id = 'n-2'
   short_edge = 1.0

   path = ShortestPathCalculator.find(
      STALE_QUEUE_GRAPH,
      start_node_id,
      end_node_id )

   assert path is not None
   assert path.length_px == short_edge + short_edge
   assert path.node_ids == [ start_node_id, via_node_id, end_node_id ]


def Test_Find_TestStaleIntermediateNode_ExpectShortestPath() -> None:
   start_node_id = 'n-1'
   via_node_id = 'n-2'
   middle_node_id = 'n-3'
   end_node_id = 'n-5'
   short_edge = 1.0
   long_edge = 50.0

   path = ShortestPathCalculator.find(
      STALE_INTERMEDIATE_GRAPH,
      start_node_id,
      end_node_id )

   assert path is not None
   assert path.length_px == short_edge + short_edge + long_edge
   assert path.node_ids == [ start_node_id, via_node_id, middle_node_id, end_node_id ]
