from __future__ import annotations

from .itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from ..routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...shared.enums import ScheduleItemKind
from ...types import Types


class ItineraryWalkRouteStopMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryWalkRouteStopRecord:
      return ItineraryWalkRouteStopRecord(
         stop_sequence=int( row[ 'STOP_SEQUENCE' ] ),
         schedule_item_kind=ScheduleItemKind.normalize( row[ 'SCHEDULE_ITEM_KIND' ] ),
         item_key=row[ 'ITEM_KEY' ],
         walk_node_id=row[ 'WALK_NODE_ID' ],
         start_time=row[ 'START_TIME' ],
         end_time=row[ 'END_TIME' ] )


   @classmethod
   def map_records(
         cls, rows: list[ Types.Row ] ) -> list[ ItineraryWalkRouteStopRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]


   @classmethod
   def map_to_walk_route_stop(
         cls,
         record: ItineraryWalkRouteStopRecord ) -> ItineraryWalkRouteStop:
      return ItineraryWalkRouteStop(
         schedule_item_kind=record.schedule_item_kind,
         item_key=record.item_key,
         walk_node_id=record.walk_node_id,
         start_time=record.start_time,
         end_time=record.end_time )


   @classmethod
   def map_to_walk_route_stops(
         cls,
         records: list[ ItineraryWalkRouteStopRecord ] ) -> list[ ItineraryWalkRouteStop ]:
      return [
         cls.map_to_walk_route_stop( record )
         for record in records
      ]
