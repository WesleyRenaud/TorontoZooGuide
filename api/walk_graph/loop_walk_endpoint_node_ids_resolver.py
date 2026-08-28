from __future__ import annotations

from .domain.attraction_route_stop import AttractionRouteStop
from .domain.map_location_kind import MapLocationKind
from .domain.master_route_loop import MasterRouteLoop
from .domain.master_route_loop_traversal_checker import MasterRouteLoopTraversalChecker
from .domain.master_route_stop import MasterRouteStop
from .domain.master_route_stop_checker import MasterRouteStopChecker
from .domain.viewing_spot_reference import ViewingSpotReference
from .map_location_walk_node_lookup import MapLocationWalkNodeLookup
from .viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


class LoopWalkEndpointNodeIdsResolver():
   @classmethod
   def resolve( cls, loop: MasterRouteLoop ) -> tuple[ str | None, str | None ]:
      if not loop.viewing_spots:
         return None, None

      return (
         cls._walk_node_id_for_route_stop( loop.viewing_spots[ 0 ] ),
         cls._walk_node_id_for_route_stop( loop.viewing_spots[ -1 ] ),
      )


   @classmethod
   def orientations(
         cls,
         loop: MasterRouteLoop ) -> list[ tuple[ str | None, str | None ] ]:
      forward_endpoints = cls.resolve( loop )

      if not MasterRouteLoopTraversalChecker.is_two_way( loop.traversal ):
         return [ forward_endpoints ]

      return [
         forward_endpoints,
         ( forward_endpoints[ 1 ], forward_endpoints[ 0 ] ),
      ]


   @classmethod
   def _walk_node_id_for_route_stop( cls, stop: MasterRouteStop ) -> str | None:
      if MasterRouteStopChecker.is_animal( stop ):
         return cls._walk_node_id_for_viewing_spot_reference( stop )

      if MasterRouteStopChecker.is_attraction( stop ):
         return cls._walk_node_id_for_attraction_route_stop( stop )

      return None


   @classmethod
   def _walk_node_id_for_viewing_spot_reference(
         cls,
         viewing_spot: ViewingSpotReference ) -> str | None:
      return ViewingSpotWalkNodeIdResolver.resolve(
         viewing_spot.species,
         viewing_spot.exhibit,
         viewing_spot.name )


   @classmethod
   def _walk_node_id_for_attraction_route_stop(
         cls,
         attraction: AttractionRouteStop ) -> str | None:
      walk_node = MapLocationWalkNodeLookup.for_map_location(
         MapLocationKind.ATTRACTION,
         attraction.name )

      if walk_node is None:
         return None

      return walk_node.walk_node_id
