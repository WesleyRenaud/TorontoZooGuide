from __future__ import annotations

from .walk_route_leg import WalkRouteLeg
from .walk_route_point import WalkRoutePoint


def append_walk_route_node_id(
      route_node_ids: list[ str ],
      node_id: str ) -> None:
   if route_node_ids and route_node_ids[ -1 ] == node_id:
      return

   route_node_ids.append( node_id )


def append_walk_route_leg_node_ids(
      route_node_ids: list[ str ],
      leg_node_ids: list[ str ] ) -> None:
   for node_id in leg_node_ids:
      append_walk_route_node_id( route_node_ids, node_id )


def inclusive_point_slices_for_walk_route_legs(
      legs: list[ WalkRouteLeg ] ) -> list[ tuple[ int, int ] ]:
   """Return inclusive (from, to) indices into the route polyline for each leg.

   The polyline concatenates leg paths and stores each join node once, so leg
   slices chain together: the next leg starts where the previous leg ended.
   """
   slices: list[ tuple[ int, int ] ] = []

   for leg in legs:
      from_point_sequence = 0 if not slices else slices[ -1 ][ 1 ]
      to_point_sequence = from_point_sequence + len( leg.node_ids ) - 1

      slices.append( ( from_point_sequence, to_point_sequence ) )

   return slices


def walk_route_node_ids_for_point_slice(
      points: list[ WalkRoutePoint ],
      *,
      from_point_sequence: int,
      to_point_sequence: int ) -> list[ str ]:
   return [
      point.node_id
      for point in points[ from_point_sequence:to_point_sequence + 1 ]
   ]
