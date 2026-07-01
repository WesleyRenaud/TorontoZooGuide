from __future__ import annotations

from .itinerary_stop import ItineraryStop
from .itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.shortest_path import shortest_path_node_ids
from .walk_route_leg import WalkRouteLeg
from .walk_route_polyline import append_walk_route_leg_node_ids


def append_return_to_entrance_walk_route_leg(
      walk_graph: WalkGraph,
      *,
      entrance_stop: ItineraryStop,
      entrance_node_id: str,
      current_node_id: str,
      route_stops: list[ ItineraryWalkRouteStop ],
      legs: list[ WalkRouteLeg ],
      route_node_ids: list[ str ] ) -> None:
   if current_node_id == entrance_node_id:
      return

   return_leg_node_ids = shortest_path_node_ids(
      walk_graph,
      current_node_id,
      entrance_node_id )

   if return_leg_node_ids is None:
      return

   legs.append(
      WalkRouteLeg(
         from_item_key=route_stops[ -1 ].item_key,
         to_item_key=entrance_stop.item_key,
         from_schedule_item_kind=route_stops[ -1 ].schedule_item_kind,
         to_schedule_item_kind=entrance_stop.schedule_item_kind,
         node_ids=tuple( return_leg_node_ids ) ) )
   append_walk_route_leg_node_ids( route_node_ids, return_leg_node_ids )
   route_stops.append(
      ItineraryWalkRouteStop.from_itinerary_stop(
         entrance_stop,
         entrance_node_id ) )
