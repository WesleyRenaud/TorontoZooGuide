from __future__ import annotations

from .itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from ..routing.walk_route_leg import WalkRouteLeg
from ..routing.walk_route_point import WalkRoutePoint
from ..routing.walk_route_polyline import walk_route_node_ids_for_point_slice
from ...shared.enums import ScheduleItemKind
from ...types import Row


def map_itinerary_walk_route_leg_record( row: Row ) -> ItineraryWalkRouteLegRecord:
   return ItineraryWalkRouteLegRecord(
      leg_sequence=int( row[ 'LEG_SEQUENCE' ] ),
      from_item_key=row[ 'FROM_ITEM_KEY' ],
      to_item_key=row[ 'TO_ITEM_KEY' ],
      from_schedule_item_kind=ScheduleItemKind.normalize(
         row[ 'FROM_SCHEDULE_ITEM_KIND' ] ),
      to_schedule_item_kind=ScheduleItemKind.normalize(
         row[ 'TO_SCHEDULE_ITEM_KIND' ] ),
      from_point_sequence=int( row[ 'FROM_POINT_SEQUENCE' ] ),
      to_point_sequence=int( row[ 'TO_POINT_SEQUENCE' ] ) )


def map_itinerary_walk_route_leg_records(
      rows: list[ Row ] ) -> list[ ItineraryWalkRouteLegRecord ]:
   return [
      map_itinerary_walk_route_leg_record( row )
      for row in rows
   ]


def map_itinerary_walk_route_leg(
      record: ItineraryWalkRouteLegRecord,
      points: list[ WalkRoutePoint ] ) -> WalkRouteLeg:
   return WalkRouteLeg(
      from_item_key=record.from_item_key,
      to_item_key=record.to_item_key,
      from_schedule_item_kind=record.from_schedule_item_kind,
      to_schedule_item_kind=record.to_schedule_item_kind,
      node_ids=walk_route_node_ids_for_point_slice(
         points,
         from_point_sequence=record.from_point_sequence,
         to_point_sequence=record.to_point_sequence ) )


def map_itinerary_walk_route_legs(
      records: list[ ItineraryWalkRouteLegRecord ],
      points: list[ WalkRoutePoint ] ) -> list[ WalkRouteLeg ]:
   return [
      map_itinerary_walk_route_leg( record, points )
      for record in records
   ]
