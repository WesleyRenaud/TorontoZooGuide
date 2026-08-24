from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey
from .walk_route_anchor import WalkRouteAnchor


@dataclass( frozen=True )
class ItineraryWalkRouteStop:
   schedule_item_kind: ScheduleItemKind
   item_key: str
   walk_node_id: str
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None

   @classmethod
   def from_walk_route_anchor(
         cls,
         anchor: WalkRouteAnchor,
         walk_node_id: str ) -> ItineraryWalkRouteStop:
      return cls(
         schedule_item_kind=anchor.schedule_item_kind,
         item_key=anchor.item_key,
         walk_node_id=walk_node_id,
         start_time=anchor.start_time,
         end_time=anchor.end_time )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'schedule_item_kind': self.schedule_item_kind.value,
         'item_key': self.item_key,
         'walk_node_id': self.walk_node_id,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
