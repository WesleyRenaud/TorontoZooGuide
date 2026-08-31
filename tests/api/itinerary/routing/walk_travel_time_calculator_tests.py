from __future__ import annotations

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
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


CHAIN_GRAPH: WalkGraph = {
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
      { 'from': 'n-2', 'to': 'n-3', 'length_px': 10.0 },
   ],
}


def Test_MinutesFromLengthPx_TestLengths_ExpectFlooredMinutes() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE

   assert WalkTravelTimeCalculator.minutes_from_length_px( 0 ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( -10 ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( 0.5 * walk_px_per_minute ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( 1.0 * walk_px_per_minute ) == 1
   assert WalkTravelTimeCalculator.minutes_from_length_px( 1.5 * walk_px_per_minute ) == 1


def Test_SecondsFromLengthPx_TestLengths_ExpectFlooredMinuteSeconds() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE

   assert WalkTravelTimeCalculator.seconds_from_length_px( 0 ) == 0
   assert WalkTravelTimeCalculator.seconds_from_length_px( 0.5 * walk_px_per_minute ) == 0
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.0 * walk_px_per_minute ) == 60
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.5 * walk_px_per_minute ) == 60
   assert WalkTravelTimeCalculator.seconds_from_length_px( 2.9 * walk_px_per_minute ) == 120


def Test_SecondsBetweenNodes_TestSameNode_ExpectZero() -> None:
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      'n-1',
      'n-1' ) == 0


def Test_SecondsBetweenNodes_TestKnownPath_ExpectFlooredSeconds() -> None:
   path = ShortestPathCalculator.find( CHAIN_GRAPH, 'n-1', 'n-3' )

   assert path is not None
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      'n-1',
      'n-3' ) == WalkTravelTimeCalculator.seconds_from_length_px( path.length_px )


def Test_SecondsForShortestPath_TestPathAndNone_ExpectSecondsOrZero() -> None:
   path = ShortestPathCalculator.find( CHAIN_GRAPH, 'n-1', 'n-3' )

   assert path is not None
   assert WalkTravelTimeCalculator.seconds_for_shortest_path( path ) == (
      WalkTravelTimeCalculator.minutes_from_length_px( path.length_px ) * 60 )
   assert WalkTravelTimeCalculator.seconds_for_shortest_path( None ) == 0


def Test_SecondsBetweenNodes_TestUnreachableNode_ExpectZero() -> None:
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      'n-1',
      'not-a-real-node' ) == 0
