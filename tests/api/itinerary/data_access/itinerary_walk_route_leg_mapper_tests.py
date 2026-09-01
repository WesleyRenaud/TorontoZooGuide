from __future__ import annotations

from api.itinerary.data_access.itinerary_walk_route_leg_mapper import ItineraryWalkRouteLegMapper
from api.itinerary.data_access.itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.enums import ScheduleItemKind


LEG_ROW = {
   'LEG_SEQUENCE': 1,
   'FROM_ITEM_KEY': 'entrance',
   'TO_ITEM_KEY': 'African Lion||Africa Savanna',
   'FROM_SCHEDULE_ITEM_KIND': 'entrance',
   'TO_SCHEDULE_ITEM_KIND': 'animal',
   'FROM_POINT_SEQUENCE': 0,
   'TO_POINT_SEQUENCE': 1,
   'TRAVEL_TIME_MINUTES': 5,
}

ROUTE_POINTS = [
   WalkRoutePoint(
      node_id='n-entrance',
      x=0.0,
      y=0.0,
      x_px=0.0,
      y_px=0.0 ),
   WalkRoutePoint(
      node_id='n-lion',
      x=10.0,
      y=10.0,
      x_px=10.0,
      y_px=10.0 ),
]


def Test_MapRecord_TestRow_ExpectLegRecord() -> None:
   assert ItineraryWalkRouteLegMapper.map_record( LEG_ROW ) == ItineraryWalkRouteLegRecord(
      leg_sequence=1,
      from_item_key='entrance',
      to_item_key='African Lion||Africa Savanna',
      from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
      to_schedule_item_kind=ScheduleItemKind.ANIMAL,
      from_point_sequence=0,
      to_point_sequence=1,
      travel_time_minutes=5,
   )


def Test_MapToWalkRouteLeg_TestRecordAndPoints_ExpectWalkRouteLeg() -> None:
   record = ItineraryWalkRouteLegRecord(
      leg_sequence=1,
      from_item_key='entrance',
      to_item_key='African Lion||Africa Savanna',
      from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
      to_schedule_item_kind=ScheduleItemKind.ANIMAL,
      from_point_sequence=0,
      to_point_sequence=1,
      travel_time_minutes=5,
   )

   assert ItineraryWalkRouteLegMapper.map_to_walk_route_leg(
      record,
      ROUTE_POINTS,
   ) == WalkRouteLeg(
      from_item_key='entrance',
      to_item_key='African Lion||Africa Savanna',
      from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
      to_schedule_item_kind=ScheduleItemKind.ANIMAL,
      node_ids=[ 'n-entrance', 'n-lion' ],
      travel_time_minutes=5,
   )
