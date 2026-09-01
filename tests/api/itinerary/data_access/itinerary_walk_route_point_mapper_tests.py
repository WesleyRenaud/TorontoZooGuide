from __future__ import annotations

from api.itinerary.data_access.itinerary_walk_route_point_mapper import ItineraryWalkRoutePointMapper
from api.itinerary.data_access.itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from api.itinerary.routing.walk_route_point import WalkRoutePoint


POINT_ROW = {
   'POINT_SEQUENCE': 0,
   'WALK_NODE_ID': 'n-1',
   'X': 0.1,
   'Y': 0.2,
   'X_PX': 10.0,
   'Y_PX': 20.0,
}


def Test_MapRecord_TestRow_ExpectPointRecord() -> None:
   assert ItineraryWalkRoutePointMapper.map_record( POINT_ROW ) == ItineraryWalkRoutePointRecord(
      point_sequence=0,
      walk_node_id='n-1',
      x=0.1,
      y=0.2,
      x_px=10.0,
      y_px=20.0,
   )


def Test_MapToWalkRoutePoint_TestRecord_ExpectWalkRoutePoint() -> None:
   record = ItineraryWalkRoutePointRecord(
      point_sequence=0,
      walk_node_id='n-1',
      x=0.1,
      y=0.2,
      x_px=10.0,
      y_px=20.0,
   )

   assert ItineraryWalkRoutePointMapper.map_to_walk_route_point( record ) == WalkRoutePoint(
      node_id='n-1',
      x=0.1,
      y=0.2,
      x_px=10.0,
      y_px=20.0,
   )
