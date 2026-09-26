from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.itinerary_walk_route_stop_mapper import ItineraryWalkRouteStopMapper
from api.itinerary.data_access.itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.shared.date_values import DateValues
from api.shared.enums import ScheduleItemKind


def Test_MapRecord_TestRow_ExpectStopRecord() -> None:
   stop_sequence = 1
   schedule_item_kind = ScheduleItemKind.ANIMAL
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   item_key = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )
   walk_node_id = 'n-lion'
   start_time = '10:00 AM'
   duration_minutes = 8
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'STOP_SEQUENCE': stop_sequence,
      'SCHEDULE_ITEM_KIND': schedule_item_kind.value,
      'ITEM_KEY': item_key,
      'WALK_NODE_ID': walk_node_id,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }

   record = ItineraryWalkRouteStopMapper.map_record( row )

   assert record == ItineraryWalkRouteStopRecord(
      stop_sequence=int( stop_sequence ),
      schedule_item_kind=ScheduleItemKind.normalize( schedule_item_kind.value ),
      item_key=item_key,
      walk_node_id=walk_node_id,
      start_time=start_time,
      end_time=end_time )


def Test_MapToWalkRouteStop_TestRecord_ExpectWalkRouteStop() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '10:00 AM'
   duration_minutes = 8
   record = ItineraryWalkRouteStopRecord(
      stop_sequence=1,
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key=AnimalScheduleItemKey.wire( species=species, exhibit=exhibit ),
      walk_node_id='n-lion',
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   stop = ItineraryWalkRouteStopMapper.map_to_walk_route_stop( record )

   assert stop == ItineraryWalkRouteStop(
      schedule_item_kind=record.schedule_item_kind,
      item_key=record.item_key,
      walk_node_id=record.walk_node_id,
      start_time=record.start_time,
      end_time=record.end_time )
