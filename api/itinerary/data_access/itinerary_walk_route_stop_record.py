from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind
from ...types import Types


@dataclass( frozen=True )
class ItineraryWalkRouteStopRecord:
   stop_sequence: int
   schedule_item_kind: ScheduleItemKind
   item_key: str
   walk_node_id: str
   start_time: Types.ScheduleTimeKey = None
   end_time: Types.ScheduleTimeKey = None
