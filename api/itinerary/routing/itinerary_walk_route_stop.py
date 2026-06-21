from __future__ import annotations

from dataclasses import dataclass

from .itinerary_stop import ItineraryStop
from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryWalkRouteStop:
   schedule_item_kind: ScheduleItemKind
   item_key: str
   walk_node_id: str | None
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None

   @classmethod
   def from_itinerary_stop(
         cls,
         stop: ItineraryStop,
         walk_node_id: str | None ) -> ItineraryWalkRouteStop:
      return cls(
         schedule_item_kind=stop.schedule_item_kind,
         item_key=stop.item_key,
         walk_node_id=walk_node_id,
         start_time=stop.start_time,
         end_time=stop.end_time )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'schedule_item_kind': self.schedule_item_kind.value,
         'item_key': self.item_key,
         'walk_node_id': self.walk_node_id,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
