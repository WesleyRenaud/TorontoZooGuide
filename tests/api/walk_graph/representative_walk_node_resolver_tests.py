from __future__ import annotations

from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.representative_walk_node_resolver import RepresentativeWalkNodeResolver

FROM_NODE_ID = 'n-1'
NEAR_NODE_ID = 'n-2'
FAR_NODE_ID = 'n-3'
UNREACHABLE_NODE_ID = 'n-4'

def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }

TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': FROM_NODE_ID,
   'nodes': [
      _node( FROM_NODE_ID, 0.0, 0.0 ),
      _node( NEAR_NODE_ID, 10.0, 0.0 ),
      _node( FAR_NODE_ID, 30.0, 0.0 ),
      _node( UNREACHABLE_NODE_ID, 50.0, 50.0 ),
   ],
   'edges': [
      { 'from': FROM_NODE_ID, 'to': NEAR_NODE_ID, 'length_px': 10.0 },
      { 'from': NEAR_NODE_ID, 'to': FROM_NODE_ID, 'length_px': 10.0 },
      { 'from': FROM_NODE_ID, 'to': FAR_NODE_ID, 'length_px': 30.0 },
      { 'from': FAR_NODE_ID, 'to': FROM_NODE_ID, 'length_px': 30.0 },
   ],
}

def Test_Resolve_TestEmptyCandidates_ExpectNone() -> None:
   assert RepresentativeWalkNodeResolver.resolve(
      TEST_GRAPH,
      FROM_NODE_ID,
      [] ) is None

def Test_Resolve_TestSingleCandidate_ExpectThatId() -> None:
   assert RepresentativeWalkNodeResolver.resolve(
      TEST_GRAPH,
      FROM_NODE_ID,
      [ FAR_NODE_ID ] ) == FAR_NODE_ID

def Test_Resolve_TestMultipleCandidates_ExpectClosest() -> None:
   assert RepresentativeWalkNodeResolver.resolve(
      TEST_GRAPH,
      FROM_NODE_ID,
      [ FAR_NODE_ID, NEAR_NODE_ID ] ) == NEAR_NODE_ID

def Test_Resolve_TestUnreachableCandidates_ExpectSkipped() -> None:
   assert RepresentativeWalkNodeResolver.resolve(
      TEST_GRAPH,
      FROM_NODE_ID,
      [ UNREACHABLE_NODE_ID, FAR_NODE_ID ] ) == FAR_NODE_ID
