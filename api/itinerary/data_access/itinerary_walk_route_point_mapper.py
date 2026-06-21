from __future__ import annotations

from collections.abc import Iterable

from .itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from ..routing.walk_route_point import WalkRoutePoint
from ...types import Row


def map_itinerary_walk_route_point_record( row: Row ) -> ItineraryWalkRoutePointRecord:
   return ItineraryWalkRoutePointRecord(
      point_sequence=int( row[ 'POINT_SEQUENCE' ] ),
      walk_node_id=row[ 'WALK_NODE_ID' ],
      x=float( row[ 'X' ] ),
      y=float( row[ 'Y' ] ),
      x_px=float( row[ 'X_PX' ] ),
      y_px=float( row[ 'Y_PX' ] ) )


def map_itinerary_walk_route_point_records(
      rows: Iterable[ Row ] ) -> list[ ItineraryWalkRoutePointRecord ]:
   return [
      map_itinerary_walk_route_point_record( row )
      for row in rows
   ]


def map_itinerary_walk_route_point(
      record: ItineraryWalkRoutePointRecord ) -> WalkRoutePoint:
   return WalkRoutePoint(
      node_id=record.walk_node_id,
      x=record.x,
      y=record.y,
      x_px=record.x_px,
      y_px=record.y_px )


def map_itinerary_walk_route_points(
      records: Iterable[ ItineraryWalkRoutePointRecord ] ) -> tuple[ WalkRoutePoint, ... ]:
   return tuple(
      map_itinerary_walk_route_point( record )
      for record in records )
