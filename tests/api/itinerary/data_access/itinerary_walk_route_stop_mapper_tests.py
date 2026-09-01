from __future__ import annotations

from api.itinerary.data_access.itinerary_walk_route_stop_mapper import ItineraryWalkRouteStopMapper
from api.itinerary.data_access.itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.shared.enums import ScheduleItemKind


STOP_ROW = {
   'STOP_SEQUENCE': 1,
   'SCHEDULE_ITEM_KIND': 'animal',
   'ITEM_KEY': 'African Lion||Africa Savanna',
   'WALK_NODE_ID': 'n-lion',
   'START_TIME': '10:00 AM',
   'END_TIME': '10:08 AM',
}


def Test_MapRecord_TestRow_ExpectStopRecord() -> None:
   assert ItineraryWalkRouteStopMapper.map_record( STOP_ROW ) == ItineraryWalkRouteStopRecord(
      stop_sequence=1,
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna',
      walk_node_id='n-lion',
      start_time='10:00 AM',
      end_time='10:08 AM',
   )


def Test_MapToWalkRouteStop_TestRecord_ExpectWalkRouteStop() -> None:
   record = ItineraryWalkRouteStopRecord(
      stop_sequence=1,
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna',
      walk_node_id='n-lion',
      start_time='10:00 AM',
      end_time='10:08 AM',
   )

   assert ItineraryWalkRouteStopMapper.map_to_walk_route_stop( record ) == ItineraryWalkRouteStop(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna',
      walk_node_id='n-lion',
      start_time='10:00 AM',
      end_time='10:08 AM',
   )
