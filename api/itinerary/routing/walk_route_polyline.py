from __future__ import annotations

from ...shared.enums.sequence_index import SequenceIndex
from .walk_route_leg import WalkRouteLeg
from .walk_route_point import WalkRoutePoint


def append_walk_route_node_id(
      route_node_ids: list[ str ],
      node_id: str ) -> None:
   if (
         route_node_ids
         and route_node_ids[ SequenceIndex.LAST ] == node_id
   ):
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

   Continuous legs share a join node stored once in the polyline. After a
   transit ride the next walk leg starts at a different node, so its slice
   begins at the next point instead of reusing the previous end.
   """
   slices: list[ tuple[ int, int ] ] = []

   for leg_index, leg in enumerate( legs ):
      if not slices:
         from_point_sequence = SequenceIndex.FIRST
      elif _legs_share_join_node( legs[ leg_index + SequenceIndex.LAST ], leg ):
         from_point_sequence = slices[ SequenceIndex.LAST ][ SequenceIndex.SECOND ]
      else:
         from_point_sequence = (
            slices[ SequenceIndex.LAST ][ SequenceIndex.SECOND ]
            + SequenceIndex.SECOND
         )

      to_point_sequence = (
         from_point_sequence + len( leg.node_ids ) + SequenceIndex.LAST
      )
      slices.append( ( from_point_sequence, to_point_sequence ) )

   return slices


def _legs_share_join_node(
      previous_leg: WalkRouteLeg,
      current_leg: WalkRouteLeg,
) -> bool:
   return (
      previous_leg.node_ids[ SequenceIndex.LAST ]
      == current_leg.node_ids[ SequenceIndex.FIRST ]
   )


def walk_route_node_ids_for_point_slice(
      points: list[ WalkRoutePoint ],
      *,
      from_point_sequence: int,
      to_point_sequence: int ) -> list[ str ]:
   return [
      point.node_id
      for point in points[
         from_point_sequence:to_point_sequence + SequenceIndex.SECOND
      ]
   ]
