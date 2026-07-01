from __future__ import annotations

from api.itinerary.routing.append_return_to_entrance_walk_route_leg import append_return_to_entrance_walk_route_leg
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path import shortest_path_node_ids


def test_append_return_to_entrance_walk_route_leg_skips_when_already_at_entrance() -> None:
   walk_graph = load_walk_graph()
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   entrance_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=( entrance_node_id, ),
      x_coord=0.0,
      y_coord=0.0 )
   route_stops = [
      ItineraryWalkRouteStop.from_itinerary_stop(
         entrance_stop,
         entrance_node_id ),
   ]
   legs = []
   route_node_ids: list[ str ] = []

   append_return_to_entrance_walk_route_leg(
      walk_graph,
      entrance_stop=entrance_stop,
      entrance_node_id=entrance_node_id,
      current_node_id=entrance_node_id,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert legs == []
   assert route_stops == [
      ItineraryWalkRouteStop.from_itinerary_stop(
         entrance_stop,
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
   entrance_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=( entrance_node_id, ),
      x_coord=0.0,
      y_coord=0.0 )
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

   append_return_to_entrance_walk_route_leg(
      walk_graph,
      entrance_stop=entrance_stop,
      entrance_node_id=entrance_node_id,
      current_node_id=sample_node_id,
      route_stops=route_stops,
      legs=legs,
      route_node_ids=route_node_ids )

   assert len( legs ) == 1
   assert legs[ 0 ].to_item_key == ENTRANCE_ITEM_KEY
   assert legs[ 0 ].node_ids == tuple( expected_node_ids )
   assert route_stops[ -1 ].item_key == ENTRANCE_ITEM_KEY
   assert route_stops[ -1 ].walk_node_id == entrance_node_id
   assert route_node_ids == list( expected_node_ids )
