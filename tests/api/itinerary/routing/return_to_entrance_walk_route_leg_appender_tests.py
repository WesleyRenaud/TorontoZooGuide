from __future__ import annotations

from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.return_to_entrance_walk_route_leg_appender import ReturnToEntranceWalkRouteLegAppender
from api.itinerary.routing.walk_route_anchor import WalkRouteAnchor
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.shared.enums import ScheduleItemKind
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


TEST_GRAPH: WalkGraph = {
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

ENTRANCE_NODE_ID = 'n-1'
DESTINATION_NODE_ID = 'n-2'

ENTRANCE_ANCHOR = WalkRouteAnchor(
   schedule_item_kind=ScheduleItemKind.ENTRANCE,
   item_key=ENTRANCE_ITEM_KEY,
   walk_node_ids=[ ENTRANCE_NODE_ID ] )


def Test_Append_TestAlreadyAtEntrance_ExpectNoLegAppended() -> None:
   route_stops = [
      ItineraryWalkRouteStop.from_walk_route_anchor(
         ENTRANCE_ANCHOR,
         ENTRANCE_NODE_ID ),
   ]
   legs: list[ WalkRouteLeg ] = []
   route_node_ids: list[ str ] = []

   ReturnToEntranceWalkRouteLegAppender.append(
      TEST_GRAPH,
      entrance_anchor=ENTRANCE_ANCHOR,
      entrance_node_id=ENTRANCE_NODE_ID,
      current_node_id=ENTRANCE_NODE_ID,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert legs == []
   assert route_stops == [
      ItineraryWalkRouteStop.from_walk_route_anchor(
         ENTRANCE_ANCHOR,
         ENTRANCE_NODE_ID ),
   ]
   assert route_node_ids == []


def Test_Append_TestAwayFromEntrance_ExpectShortestPathLegAppended() -> None:
   from_stop = ItineraryWalkRouteStop(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='Lion||Africa Savanna',
      walk_node_id=DESTINATION_NODE_ID )
   route_stops = [ from_stop ]
   legs: list[ WalkRouteLeg ] = []
   route_node_ids: list[ str ] = []
   expected_node_ids = ShortestPathCalculator.node_ids(
      TEST_GRAPH,
      DESTINATION_NODE_ID,
      ENTRANCE_NODE_ID )

   assert expected_node_ids is not None

   ReturnToEntranceWalkRouteLegAppender.append(
      TEST_GRAPH,
      entrance_anchor=ENTRANCE_ANCHOR,
      entrance_node_id=ENTRANCE_NODE_ID,
      current_node_id=DESTINATION_NODE_ID,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert len( legs ) == 1
   assert legs[ 0 ].to_item_key == ENTRANCE_ITEM_KEY
   assert legs[ 0 ].node_ids == expected_node_ids
   assert route_stops[ -1 ].item_key == ENTRANCE_ITEM_KEY
   assert route_stops[ -1 ].walk_node_id == ENTRANCE_NODE_ID
   assert route_node_ids == list( expected_node_ids )
