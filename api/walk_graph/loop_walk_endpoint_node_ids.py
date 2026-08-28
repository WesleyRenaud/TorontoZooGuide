from __future__ import annotations

from .domain.attraction_route_stop import AttractionRouteStop
from .domain.map_location_kind import MapLocationKind
from .domain.master_route_loop import is_two_way_loop_traversal
from .domain.master_route_loop import MasterRouteLoop
from .domain.master_route_stop import is_animal_route_stop
from .domain.master_route_stop import is_attraction_route_stop
from .domain.master_route_stop import MasterRouteStop
from .domain.viewing_spot_reference import ViewingSpotReference
from .map_location_walk_node_lookup import walk_node_for_map_location
from .viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


def loop_walk_endpoint_node_ids(
      loop: MasterRouteLoop ) -> tuple[ str | None, str | None ]:
   if not loop.viewing_spots:
      return None, None

   return (
      _walk_node_id_for_route_stop( loop.viewing_spots[ 0 ] ),
      _walk_node_id_for_route_stop( loop.viewing_spots[ -1 ] ),
   )


def loop_walk_endpoint_orientations(
      loop: MasterRouteLoop ) -> list[ tuple[ str | None, str | None ] ]:
   forward_endpoints = loop_walk_endpoint_node_ids( loop )

   if not is_two_way_loop_traversal( loop.traversal ):
      return [ forward_endpoints ]

   return [
      forward_endpoints,
      ( forward_endpoints[ 1 ], forward_endpoints[ 0 ] ),
   ]


def _walk_node_id_for_route_stop( stop: MasterRouteStop ) -> str | None:
   if is_animal_route_stop( stop ):
      return _walk_node_id_for_viewing_spot_reference( stop )

   if is_attraction_route_stop( stop ):
      return _walk_node_id_for_attraction_route_stop( stop )

   return None


def _walk_node_id_for_viewing_spot_reference(
      viewing_spot: ViewingSpotReference ) -> str | None:
   return ViewingSpotWalkNodeIdResolver.resolve(
      viewing_spot.species,
      viewing_spot.exhibit,
      viewing_spot.name )


def _walk_node_id_for_attraction_route_stop(
      attraction: AttractionRouteStop ) -> str | None:
   walk_node = walk_node_for_map_location(
      MapLocationKind.ATTRACTION,
      attraction.name )

   if walk_node is None:
      return None

   return walk_node.walk_node_id
