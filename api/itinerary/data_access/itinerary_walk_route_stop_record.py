from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryWalkRouteStopRecord:
   stop_sequence: int
   schedule_item_kind: ScheduleItemKind
   item_key: str
   walk_node_id: str
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None
