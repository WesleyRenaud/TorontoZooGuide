from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey

ENTRANCE_ITEM_KEY = 'entrance'


@dataclass( frozen=True )
class ItineraryStop:
   walk_node_ids: list[ str ]
   schedule_item_kind: ScheduleItemKind
   item_key: str
   meeting_spot: str | None = None
   x_coord: float | None = None
   y_coord: float | None = None
   is_fixed_time: bool = False
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None


   def primary_walk_node_id( self ) -> str | None:
      if not self.walk_node_ids:
         return None

      return self.walk_node_ids[ 0 ]
