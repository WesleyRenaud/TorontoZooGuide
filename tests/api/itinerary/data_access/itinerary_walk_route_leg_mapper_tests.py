from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.itinerary_walk_route_leg_mapper import ItineraryWalkRouteLegMapper
from api.itinerary.data_access.itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.itinerary.routing.walk_route_polyline_builder import WalkRoutePolylineBuilder
from api.shared.enums import ScheduleItemKind
from api.shared.enums.position import Position


def Test_MapRecord_TestRow_ExpectLegRecord() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   from_item_key = 'entrance'
   to_item_key = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )
   from_schedule_item_kind = ScheduleItemKind.ENTRANCE
   to_schedule_item_kind = ScheduleItemKind.ANIMAL
   from_point_sequence = Position.FIRST
   to_point_sequence = Position.SECOND
   travel_time_minutes = 5
   leg_sequence = 1
   row = {
      'LEG_SEQUENCE': leg_sequence,
      'FROM_ITEM_KEY': from_item_key,
      'TO_ITEM_KEY': to_item_key,
      'FROM_SCHEDULE_ITEM_KIND': from_schedule_item_kind.value,
      'TO_SCHEDULE_ITEM_KIND': to_schedule_item_kind.value,
      'FROM_POINT_SEQUENCE': from_point_sequence,
      'TO_POINT_SEQUENCE': to_point_sequence,
      'TRAVEL_TIME_MINUTES': travel_time_minutes,
   }

   record = ItineraryWalkRouteLegMapper.map_record( row )

   assert record == ItineraryWalkRouteLegRecord(
      leg_sequence=int( leg_sequence ),
      from_item_key=from_item_key,
      to_item_key=to_item_key,
      from_schedule_item_kind=ScheduleItemKind.normalize(
         from_schedule_item_kind.value ),
      to_schedule_item_kind=ScheduleItemKind.normalize(
         to_schedule_item_kind.value ),
      from_point_sequence=int( from_point_sequence ),
      to_point_sequence=int( to_point_sequence ),
      travel_time_minutes=int( travel_time_minutes ) )


def Test_MapToWalkRouteLeg_TestRecordAndPoints_ExpectWalkRouteLeg() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   from_item_key = 'entrance'
   to_item_key = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )
   from_point_sequence = Position.FIRST
   to_point_sequence = Position.SECOND
   travel_time_minutes = 5
   entrance_point = WalkRoutePoint(
      node_id='n-entrance',
      x=0.0,
      y=0.0,
      x_px=0.0,
      y_px=0.0 )
   lion_point = WalkRoutePoint(
      node_id='n-lion',
      x=10.0,
      y=10.0,
      x_px=10.0,
      y_px=10.0 )
   route_points = [ entrance_point, lion_point ]
   record = ItineraryWalkRouteLegRecord(
      leg_sequence=1,
      from_item_key=from_item_key,
      to_item_key=to_item_key,
      from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
      to_schedule_item_kind=ScheduleItemKind.ANIMAL,
      from_point_sequence=from_point_sequence,
      to_point_sequence=to_point_sequence,
      travel_time_minutes=travel_time_minutes )

   leg = ItineraryWalkRouteLegMapper.map_to_walk_route_leg(
      record,
      route_points )

   assert leg == WalkRouteLeg(
      from_item_key=record.from_item_key,
      to_item_key=record.to_item_key,
      from_schedule_item_kind=record.from_schedule_item_kind,
      to_schedule_item_kind=record.to_schedule_item_kind,
      node_ids=WalkRoutePolylineBuilder.node_ids_for_point_slice(
         route_points,
         from_point_sequence=record.from_point_sequence,
         to_point_sequence=record.to_point_sequence ),
      travel_time_minutes=record.travel_time_minutes )
