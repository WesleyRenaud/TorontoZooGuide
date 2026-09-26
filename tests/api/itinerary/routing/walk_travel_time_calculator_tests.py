from __future__ import annotations

import math

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.shared.duration_values import DurationValues
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator


START_NODE_ID = 'n-1'
MIDDLE_NODE_ID = 'n-2'
END_NODE_ID = 'n-3'
UNKNOWN_NODE_ID = 'not-a-real-node'


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
   'entrance_node_id': START_NODE_ID,
   'nodes': [
      _node( START_NODE_ID, 0.0, 0.0 ),
      _node( MIDDLE_NODE_ID, 10.0, 0.0 ),
      _node( END_NODE_ID, 20.0, 0.0 ),
   ],
   'edges': [
      { 'from': START_NODE_ID, 'to': MIDDLE_NODE_ID, 'length_px': 10.0 },
      { 'from': MIDDLE_NODE_ID, 'to': END_NODE_ID, 'length_px': 10.0 },
   ],
}


def Test_MinutesFromLengthPx_TestZero_ExpectZero() -> None:
   length_px = 0

   minutes = WalkTravelTimeCalculator.minutes_from_length_px( length_px )

   assert minutes == 0


def Test_MinutesFromLengthPx_TestNegative_ExpectZero() -> None:
   length_px = -10

   minutes = WalkTravelTimeCalculator.minutes_from_length_px( length_px )

   assert minutes == 0


def Test_MinutesFromLengthPx_TestHalfMinute_ExpectZero() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 0.5 * walk_px_per_minute

   minutes = WalkTravelTimeCalculator.minutes_from_length_px( length_px )

   assert minutes == math.floor( length_px / walk_px_per_minute )


def Test_MinutesFromLengthPx_TestOneMinute_ExpectFloored() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 1.0 * walk_px_per_minute

   minutes = WalkTravelTimeCalculator.minutes_from_length_px( length_px )

   assert minutes == math.floor( length_px / walk_px_per_minute )


def Test_MinutesFromLengthPx_TestOneAndHalfMinutes_ExpectFloored() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 1.5 * walk_px_per_minute

   minutes = WalkTravelTimeCalculator.minutes_from_length_px( length_px )

   assert minutes == math.floor( length_px / walk_px_per_minute )


def Test_SecondsFromLengthPx_TestZero_ExpectZero() -> None:
   length_px = 0

   seconds = WalkTravelTimeCalculator.seconds_from_length_px( length_px )

   assert seconds == 0


def Test_SecondsFromLengthPx_TestHalfMinute_ExpectZero() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 0.5 * walk_px_per_minute

   seconds = WalkTravelTimeCalculator.seconds_from_length_px( length_px )

   assert seconds == DurationValues.minutes_to_seconds(
      math.floor( length_px / walk_px_per_minute ) )


def Test_SecondsFromLengthPx_TestOneMinute_ExpectFlooredMinuteSeconds() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 1.0 * walk_px_per_minute

   seconds = WalkTravelTimeCalculator.seconds_from_length_px( length_px )

   assert seconds == DurationValues.minutes_to_seconds(
      math.floor( length_px / walk_px_per_minute ) )


def Test_SecondsFromLengthPx_TestOneAndHalfMinutes_ExpectFlooredMinuteSeconds() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 1.5 * walk_px_per_minute

   seconds = WalkTravelTimeCalculator.seconds_from_length_px( length_px )

   assert seconds == DurationValues.minutes_to_seconds(
      math.floor( length_px / walk_px_per_minute ) )


def Test_SecondsFromLengthPx_TestTwoPointNineMinutes_ExpectFlooredMinuteSeconds() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE
   length_px = 2.9 * walk_px_per_minute

   seconds = WalkTravelTimeCalculator.seconds_from_length_px( length_px )

   assert seconds == DurationValues.minutes_to_seconds(
      math.floor( length_px / walk_px_per_minute ) )


def Test_SecondsBetweenNodes_TestSameNode_ExpectZero() -> None:
   seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      START_NODE_ID,
      START_NODE_ID )

   assert seconds == 0


def Test_SecondsBetweenNodes_TestKnownPath_ExpectFlooredSeconds() -> None:
   path = ShortestPathCalculator.find( CHAIN_GRAPH, START_NODE_ID, END_NODE_ID )

   seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      START_NODE_ID,
      END_NODE_ID )

   assert path is not None
   assert seconds == WalkTravelTimeCalculator.seconds_from_length_px( path.length_px )


def Test_SecondsForShortestPath_TestKnownPath_ExpectFlooredSeconds() -> None:
   path = ShortestPathCalculator.find( CHAIN_GRAPH, START_NODE_ID, END_NODE_ID )

   seconds = WalkTravelTimeCalculator.seconds_for_shortest_path( path )

   assert path is not None
   assert seconds == WalkTravelTimeCalculator.seconds_from_length_px( path.length_px )


def Test_SecondsForShortestPath_TestNone_ExpectZero() -> None:
   path = None

   seconds = WalkTravelTimeCalculator.seconds_for_shortest_path( path )

   assert seconds == 0


def Test_SecondsBetweenNodes_TestUnreachableNode_ExpectZero() -> None:
   seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      CHAIN_GRAPH,
      START_NODE_ID,
      UNKNOWN_NODE_ID )

   assert seconds == 0
