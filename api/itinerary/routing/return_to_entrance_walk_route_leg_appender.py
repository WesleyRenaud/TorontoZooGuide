from __future__ import annotations

from .itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.shortest_path import WalkGraphAdjacency
from ...walk_graph.shortest_path_calculator import ShortestPathCalculator
from .walk_route_anchor import WalkRouteAnchor
from .walk_route_leg import WalkRouteLeg
from .walk_route_polyline_builder import WalkRoutePolylineBuilder
from .walk_travel_time_calculator import WalkTravelTimeCalculator


class ReturnToEntranceWalkRouteLegAppender():
   @classmethod
   def append(
         cls,
         walk_graph: WalkGraph,
         *,
         entrance_anchor: WalkRouteAnchor,
         entrance_node_id: str,
         current_node_id: str,
         route_stops: list[ ItineraryWalkRouteStop ],
         legs: list[ WalkRouteLeg ],
         route_node_ids: list[ str ],
         adjacency: WalkGraphAdjacency | None = None ) -> None:
      if current_node_id == entrance_node_id:
         return

      return_leg_path = ShortestPathCalculator.find(
         walk_graph,
         current_node_id,
         entrance_node_id,
         adjacency=adjacency )

      if return_leg_path is None:
         return

      legs.append(
         WalkTravelTimeCalculator.route_leg_with_travel_time(
            from_item_key=route_stops[ -1 ].item_key,
            to_item_key=entrance_anchor.item_key,
            from_schedule_item_kind=route_stops[ -1 ].schedule_item_kind,
            to_schedule_item_kind=entrance_anchor.schedule_item_kind,
            node_ids=return_leg_path.node_ids,
            length_px=return_leg_path.length_px ) )
      WalkRoutePolylineBuilder.append_leg_node_ids(
         route_node_ids,
         return_leg_path.node_ids )
      route_stops.append(
         ItineraryWalkRouteStop.from_walk_route_anchor(
            entrance_anchor,
            entrance_node_id ) )
