from __future__ import annotations

from .itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from ..routing.walk_route_leg import WalkRouteLeg
from ..routing.walk_route_point import WalkRoutePoint
from ..routing.walk_route_polyline_builder import WalkRoutePolylineBuilder
from ...shared.enums import ScheduleItemKind
from ...types import Types


class ItineraryWalkRouteLegMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryWalkRouteLegRecord:
      return ItineraryWalkRouteLegRecord(
         leg_sequence=int( row[ 'LEG_SEQUENCE' ] ),
         from_item_key=row[ 'FROM_ITEM_KEY' ],
         to_item_key=row[ 'TO_ITEM_KEY' ],
         from_schedule_item_kind=ScheduleItemKind.normalize(
            row[ 'FROM_SCHEDULE_ITEM_KIND' ] ),
         to_schedule_item_kind=ScheduleItemKind.normalize(
            row[ 'TO_SCHEDULE_ITEM_KIND' ] ),
         from_point_sequence=int( row[ 'FROM_POINT_SEQUENCE' ] ),
         to_point_sequence=int( row[ 'TO_POINT_SEQUENCE' ] ),
         travel_time_minutes=int( row[ 'TRAVEL_TIME_MINUTES' ] ) )


   @classmethod
   def map_records(
         cls, rows: list[ Types.Row ] ) -> list[ ItineraryWalkRouteLegRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]


   @classmethod
   def map_to_walk_route_leg(
         cls,
         record: ItineraryWalkRouteLegRecord,
         points: list[ WalkRoutePoint ] ) -> WalkRouteLeg:
      return WalkRouteLeg(
         from_item_key=record.from_item_key,
         to_item_key=record.to_item_key,
         from_schedule_item_kind=record.from_schedule_item_kind,
         to_schedule_item_kind=record.to_schedule_item_kind,
         node_ids=WalkRoutePolylineBuilder.node_ids_for_point_slice(
            points,
            from_point_sequence=record.from_point_sequence,
            to_point_sequence=record.to_point_sequence ),
         travel_time_minutes=record.travel_time_minutes )


   @classmethod
   def map_to_walk_route_legs(
         cls,
         records: list[ ItineraryWalkRouteLegRecord ],
         points: list[ WalkRoutePoint ] ) -> list[ WalkRouteLeg ]:
      return [
         cls.map_to_walk_route_leg( record, points )
         for record in records
      ]
