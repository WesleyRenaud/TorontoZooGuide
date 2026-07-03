from __future__ import annotations

from ..animal_item_key import parse_animal_schedule_item_key
from .append_return_to_entrance_walk_route_leg import append_return_to_entrance_walk_route_leg
from .itinerary_stop import ItineraryStop
from .itinerary_walk_route import empty_itinerary_walk_route
from .itinerary_walk_route import ItineraryWalkRoute
from .itinerary_walk_route_completion import should_append_return_to_entrance_walk_route_leg
from .itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...models import Itinerary
from .order_itinerary_stops_for_walk_route import order_itinerary_stops_for_walk_route
from .resolve_itinerary_stops import resolve_itinerary_stops
from ...shared.enums import ScheduleItemKind
from ...walk_graph.data_access.load_walk_graph import load_walk_graph
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.domain.walk_graph_node import WalkGraphNode
from ...walk_graph.representative_walk_node import representative_walk_node_id_from_candidates
from ...walk_graph.shortest_path import shortest_path_node_ids
from .walk_route_leg import WalkRouteLeg
from .walk_route_point import WalkRoutePoint
from .walk_route_polyline import append_walk_route_leg_node_ids


def build_itinerary_walk_route( itinerary: Itinerary ) -> ItineraryWalkRoute:
   ordered_stops = order_itinerary_stops_for_walk_route(
      resolve_itinerary_stops( itinerary ) )

   if not ordered_stops:
      return empty_itinerary_walk_route()

   walk_graph = load_walk_graph()
   nodes_by_id = _walk_graph_nodes_by_id( walk_graph )
   route_stops: list[ ItineraryWalkRouteStop ] = []
   legs: list[ WalkRouteLeg ] = []
   route_node_ids: list[ str ] = []
   entrance_stop, current_node_id = _resolve_entrance_walk_route_start(
      ordered_stops )
   entrance_node_id = entrance_stop.walk_node_ids[ 0 ]

   route_stops.append(
      ItineraryWalkRouteStop.from_itinerary_stop(
         entrance_stop,
         current_node_id ) )

   for next_stop in ordered_stops[ 1: ]:
      next_node_id = _resolve_itinerary_stop_walk_node_id(
         walk_graph,
         from_node_id=current_node_id,
         stop=next_stop )

      if next_node_id is None:
         continue

      leg_node_ids = shortest_path_node_ids(
         walk_graph,
         current_node_id,
         next_node_id )

      if leg_node_ids is None:
         continue

      legs.append(
         WalkRouteLeg(
            from_item_key=route_stops[ -1 ].item_key,
            to_item_key=next_stop.item_key,
            from_schedule_item_kind=route_stops[ -1 ].schedule_item_kind,
            to_schedule_item_kind=next_stop.schedule_item_kind,
            node_ids=tuple( leg_node_ids ) ) )
      append_walk_route_leg_node_ids( route_node_ids, leg_node_ids )
      route_stops.append(
         ItineraryWalkRouteStop.from_itinerary_stop(
            next_stop,
            next_node_id ) )
      current_node_id = next_node_id

   if not legs:
      return empty_itinerary_walk_route()

   if should_append_return_to_entrance_walk_route_leg( itinerary ):
      append_return_to_entrance_walk_route_leg(
         walk_graph,
         entrance_stop=entrance_stop,
         entrance_node_id=entrance_node_id,
         current_node_id=current_node_id,
         route_stops=route_stops,
         legs=legs,
         route_node_ids=route_node_ids )

   return ItineraryWalkRoute(
      stops=tuple( route_stops ),
      legs=tuple( legs ),
      points=_walk_route_points_from_node_ids(
         route_node_ids,
         nodes_by_id ) )


def _resolve_entrance_walk_route_start(
      ordered_stops: list[ ItineraryStop ] ) -> tuple[ ItineraryStop, str ]:
   entrance_stop = ordered_stops[ 0 ]

   return entrance_stop, entrance_stop.walk_node_ids[ 0 ]


def _resolve_itinerary_stop_walk_node_id(
      walk_graph: WalkGraph,
      *,
      from_node_id: str,
      stop: ItineraryStop ) -> str | None:
   if not stop.walk_node_ids:
      return None

   if len( stop.walk_node_ids ) == 1:
      return stop.walk_node_ids[ 0 ]

   if stop.schedule_item_kind == ScheduleItemKind.ANIMAL:
      parsed_key = parse_animal_schedule_item_key( stop.item_key )

      if parsed_key is not None:
         return representative_walk_node_id_from_candidates(
            walk_graph,
            from_node_id,
            stop.walk_node_ids )

   return representative_walk_node_id_from_candidates(
      walk_graph,
      from_node_id,
      stop.walk_node_ids )


def _walk_graph_nodes_by_id(
      walk_graph: WalkGraph ) -> dict[ str, WalkGraphNode ]:
   return {
      str( node[ 'id' ] ): node
      for node in walk_graph[ 'nodes' ]
   }


def _walk_route_points_from_node_ids(
      node_ids: list[ str ],
      nodes_by_id: dict[ str, WalkGraphNode ] ) -> tuple[ WalkRoutePoint, ... ]:
   points: list[ WalkRoutePoint ] = []

   for node_id in node_ids:
      node = nodes_by_id.get( node_id )

      if node is None:
         continue

      points.append( WalkRoutePoint.from_walk_graph_node( node ) )

   return tuple( points )
