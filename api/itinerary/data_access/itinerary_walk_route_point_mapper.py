from __future__ import annotations

from .itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from ..routing.walk_route_point import WalkRoutePoint
from ...types import Types


class ItineraryWalkRoutePointMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryWalkRoutePointRecord:
      return ItineraryWalkRoutePointRecord(
         point_sequence=int( row[ 'POINT_SEQUENCE' ] ),
         walk_node_id=row[ 'WALK_NODE_ID' ],
         x=float( row[ 'X' ] ),
         y=float( row[ 'Y' ] ),
         x_px=float( row[ 'X_PX' ] ),
         y_px=float( row[ 'Y_PX' ] ) )


   @classmethod
   def map_records(
         cls, rows: list[ Types.Row ] ) -> list[ ItineraryWalkRoutePointRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]


   @classmethod
   def map_to_walk_route_point(
         cls,
         record: ItineraryWalkRoutePointRecord ) -> WalkRoutePoint:
      return WalkRoutePoint(
         node_id=record.walk_node_id,
         x=record.x,
         y=record.y,
         x_px=record.x_px,
         y_px=record.y_px )


   @classmethod
   def map_to_walk_route_points(
         cls,
         records: list[ ItineraryWalkRoutePointRecord ] ) -> list[ WalkRoutePoint ]:
      return [
         cls.map_to_walk_route_point( record )
         for record in records
      ]
