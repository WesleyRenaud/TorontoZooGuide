from __future__ import annotations

from api.itinerary.data_access.itinerary_walk_route_point_mapper import ItineraryWalkRoutePointMapper
from api.itinerary.data_access.itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.enums.position import Position


def Test_MapRecord_TestRow_ExpectPointRecord() -> None:
   point_sequence = Position.FIRST
   walk_node_id = 'n-1'
   x = 0.1
   y = 0.2
   x_px = 10.0
   y_px = 20.0
   row = {
      'POINT_SEQUENCE': point_sequence,
      'WALK_NODE_ID': walk_node_id,
      'X': x,
      'Y': y,
      'X_PX': x_px,
      'Y_PX': y_px,
   }

   record = ItineraryWalkRoutePointMapper.map_record( row )

   assert record == ItineraryWalkRoutePointRecord(
      point_sequence=int( point_sequence ),
      walk_node_id=walk_node_id,
      x=float( x ),
      y=float( y ),
      x_px=float( x_px ),
      y_px=float( y_px ) )


def Test_MapToWalkRoutePoint_TestRecord_ExpectWalkRoutePoint() -> None:
   walk_node_id = 'n-1'
   x = 0.1
   y = 0.2
   x_px = 10.0
   y_px = 20.0
   record = ItineraryWalkRoutePointRecord(
      point_sequence=Position.FIRST,
      walk_node_id=walk_node_id,
      x=x,
      y=y,
      x_px=x_px,
      y_px=y_px )

   point = ItineraryWalkRoutePointMapper.map_to_walk_route_point( record )

   assert point == WalkRoutePoint(
      node_id=record.walk_node_id,
      x=record.x,
      y=record.y,
      x_px=record.x_px,
      y_px=record.y_px )
