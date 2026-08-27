from __future__ import annotations

from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.return_to_entrance_walk_route_leg_appender import ReturnToEntranceWalkRouteLegAppender
from api.itinerary.routing.walk_route_anchor import WalkRouteAnchor
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path import shortest_path_node_ids


def test_append_return_to_entrance_walk_route_leg_skips_when_already_at_entrance() -> None:
   walk_graph = load_walk_graph()
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   entrance_anchor = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=[ entrance_node_id ] )
   route_stops = [
      ItineraryWalkRouteStop.from_walk_route_anchor(
         entrance_anchor,
         entrance_node_id ),
   ]
   legs = []
   route_node_ids: list[ str ] = []

   ReturnToEntranceWalkRouteLegAppender.append(
      walk_graph,
      entrance_anchor=entrance_anchor,
      entrance_node_id=entrance_node_id,
      current_node_id=entrance_node_id,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert legs == []
   assert route_stops == [
      ItineraryWalkRouteStop.from_walk_route_anchor(
         entrance_anchor,
         entrance_node_id ),
   ]
   assert route_node_ids == []


def test_append_return_to_entrance_walk_route_leg_appends_shortest_path_back() -> None:
   walk_graph = load_walk_graph()
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   sample_node_id = next(
      node[ 'id' ]
      for node in walk_graph[ 'nodes' ]
      if node[ 'id' ] != entrance_node_id )
   entrance_anchor = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=[ entrance_node_id ] )
   from_stop = ItineraryWalkRouteStop(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='Lion||African Savanna',
      walk_node_id=sample_node_id )
   route_stops = [ from_stop ]
   legs = []
   route_node_ids: list[ str ] = []
   expected_node_ids = shortest_path_node_ids(
      walk_graph,
      sample_node_id,
      entrance_node_id )

   assert expected_node_ids is not None

   ReturnToEntranceWalkRouteLegAppender.append(
      walk_graph,
      entrance_anchor=entrance_anchor,
      entrance_node_id=entrance_node_id,
      current_node_id=sample_node_id,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert len( legs ) == 1
   assert legs[ 0 ].to_item_key == ENTRANCE_ITEM_KEY
   assert legs[ 0 ].node_ids == expected_node_ids
   assert route_stops[ -1 ].item_key == ENTRANCE_ITEM_KEY
   assert route_stops[ -1 ].walk_node_id == entrance_node_id
   assert route_node_ids == list( expected_node_ids )
