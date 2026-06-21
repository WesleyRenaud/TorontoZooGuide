from __future__ import annotations

from collections.abc import Iterable

from .itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from ..routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from ...shared.enums import ScheduleItemKind
from ...types import Row


def map_itinerary_walk_route_stop_record( row: Row ) -> ItineraryWalkRouteStopRecord:
   return ItineraryWalkRouteStopRecord(
      stop_sequence=int( row[ 'STOP_SEQUENCE' ] ),
      schedule_item_kind=ScheduleItemKind.normalize( row[ 'SCHEDULE_ITEM_KIND' ] ),
      item_key=row[ 'ITEM_KEY' ],
      walk_node_id=row[ 'WALK_NODE_ID' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ] )


def map_itinerary_walk_route_stop_records(
      rows: Iterable[ Row ] ) -> list[ ItineraryWalkRouteStopRecord ]:
   return [
      map_itinerary_walk_route_stop_record( row )
      for row in rows
   ]


def map_itinerary_walk_route_stop(
      record: ItineraryWalkRouteStopRecord ) -> ItineraryWalkRouteStop:
   return ItineraryWalkRouteStop(
      schedule_item_kind=record.schedule_item_kind,
      item_key=record.item_key,
      walk_node_id=record.walk_node_id,
      start_time=record.start_time,
      end_time=record.end_time )


def map_itinerary_walk_route_stops(
      records: Iterable[ ItineraryWalkRouteStopRecord ] ) -> tuple[ ItineraryWalkRouteStop, ... ]:
   return tuple(
      map_itinerary_walk_route_stop( record )
      for record in records )
