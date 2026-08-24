from __future__ import annotations

from ..animal_item_key import parse_animal_schedule_item_key
from .append_return_to_entrance_walk_route_leg import append_return_to_entrance_walk_route_leg
from .build_walk_route_anchors import build_walk_route_anchors
from .itinerary_walk_route import empty_itinerary_walk_route
from .itinerary_walk_route import ItineraryWalkRoute
from .itinerary_walk_route_completion import should_append_return_to_entrance_walk_route_leg
from .itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...models import Itinerary
from ...shared.enums import ScheduleItemKind
from ...walk_graph.data_access.load_walk_graph import load_walk_graph
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.domain.walk_graph_node import WalkGraphNode
from ...walk_graph.representative_walk_node import representative_walk_node_id_from_candidates
from ...walk_graph.shortest_path import build_walk_graph_adjacency
from ...walk_graph.shortest_path import shortest_path
from .walk_route_anchor import is_transit_station_ride_gap
from .walk_route_anchor import WalkRouteAnchor
from .walk_route_leg import WalkRouteLeg
from .walk_route_point import WalkRoutePoint
from .walk_route_polyline import append_walk_route_leg_node_ids
from .walk_travel_time import walk_route_leg_with_travel_time


def build_itinerary_walk_route( itinerary: Itinerary ) -> ItineraryWalkRoute:
   ordered_anchors = build_walk_route_anchors( itinerary )

   if not ordered_anchors:
      return empty_itinerary_walk_route()

   walk_graph = load_walk_graph()
   adjacency = build_walk_graph_adjacency( walk_graph )
   nodes_by_id = _walk_graph_nodes_by_id( walk_graph )
   route_stops: list[ ItineraryWalkRouteStop ] = []
   legs: list[ WalkRouteLeg ] = []
   route_node_ids: list[ str ] = []
   entrance_anchor = ordered_anchors[ 0 ]
   current_node_id = entrance_anchor.walk_node_ids[ 0 ]
   entrance_node_id = current_node_id
   previous_anchor = entrance_anchor

   route_stops.append(
      ItineraryWalkRouteStop.from_walk_route_anchor(
         entrance_anchor,
         current_node_id ) )

   for next_anchor in ordered_anchors[ 1: ]:
      next_node_id = _resolve_walk_route_anchor_node_id(
         walk_graph,
         from_node_id=current_node_id,
         anchor=next_anchor )

      if next_node_id is None:
         continue

      if is_transit_station_ride_gap( previous_anchor, next_anchor ):
         route_stops.append(
            ItineraryWalkRouteStop.from_walk_route_anchor(
               next_anchor,
               next_node_id ) )
         current_node_id = next_node_id
         previous_anchor = next_anchor
         continue

      leg_path = shortest_path(
         walk_graph,
         current_node_id,
         next_node_id,
         adjacency=adjacency )

      if leg_path is None:
         continue

      legs.append(
         walk_route_leg_with_travel_time(
            from_item_key=route_stops[ -1 ].item_key,
            to_item_key=next_anchor.item_key,
            from_schedule_item_kind=route_stops[ -1 ].schedule_item_kind,
            to_schedule_item_kind=next_anchor.schedule_item_kind,
            node_ids=leg_path.node_ids,
            length_px=leg_path.length_px ) )
      append_walk_route_leg_node_ids( route_node_ids, leg_path.node_ids )
      route_stops.append(
         ItineraryWalkRouteStop.from_walk_route_anchor(
            next_anchor,
            next_node_id ) )
      current_node_id = next_node_id
      previous_anchor = next_anchor

   if not legs:
      return empty_itinerary_walk_route()

   if should_append_return_to_entrance_walk_route_leg( itinerary ):
      append_return_to_entrance_walk_route_leg(
         walk_graph,
         entrance_anchor=entrance_anchor,
         entrance_node_id=entrance_node_id,
         current_node_id=current_node_id,
         route_stops=route_stops,
         legs=legs,
         route_node_ids=route_node_ids,
         adjacency=adjacency )

   return ItineraryWalkRoute(
      stops=route_stops,
      legs=legs,
      points=_walk_route_points_from_node_ids(
         route_node_ids,
         nodes_by_id ) )


def _resolve_walk_route_anchor_node_id(
      walk_graph: WalkGraph,
      *,
      from_node_id: str,
      anchor: WalkRouteAnchor ) -> str | None:
   if not anchor.walk_node_ids:
      return None

   if len( anchor.walk_node_ids ) == 1:
      return anchor.walk_node_ids[ 0 ]

   if anchor.schedule_item_kind == ScheduleItemKind.ANIMAL:
      parsed_key = parse_animal_schedule_item_key( anchor.item_key )

      if parsed_key is not None:
         return representative_walk_node_id_from_candidates(
            walk_graph,
            from_node_id,
            anchor.walk_node_ids )

   return representative_walk_node_id_from_candidates(
      walk_graph,
      from_node_id,
      anchor.walk_node_ids )


def _walk_graph_nodes_by_id(
      walk_graph: WalkGraph ) -> dict[ str, WalkGraphNode ]:
   return {
      str( node[ 'id' ] ): node
      for node in walk_graph[ 'nodes' ]
   }


def _walk_route_points_from_node_ids(
      node_ids: list[ str ],
      nodes_by_id: dict[ str, WalkGraphNode ] ) -> list[ WalkRoutePoint ]:
   points: list[ WalkRoutePoint ] = []

   for node_id in node_ids:
      node = nodes_by_id.get( node_id )

      if node is None:
         continue

      points.append( WalkRoutePoint.from_walk_graph_node( node ) )

   return points
