from __future__ import annotations

from ...shared.enums import ScheduleItemKind
from .walk_route_leg import WalkRouteLeg

# Calibrated so entrance → Grizzly Bear (~4548 px) is ~31 minutes.
WALK_PX_PER_MINUTE = 4548 / 31


def travel_time_minutes_from_length_px( length_px: float ) -> int:
   if length_px <= 0:
      return 0

   return round( length_px / WALK_PX_PER_MINUTE )


def walk_route_leg_with_travel_time(
      *,
      from_item_key: str,
      to_item_key: str,
      from_schedule_item_kind: ScheduleItemKind,
      to_schedule_item_kind: ScheduleItemKind,
      node_ids: list[ str ],
      length_px: float ) -> WalkRouteLeg:
   return WalkRouteLeg(
      from_item_key=from_item_key,
      to_item_key=to_item_key,
      from_schedule_item_kind=from_schedule_item_kind,
      to_schedule_item_kind=to_schedule_item_kind,
      node_ids=node_ids,
      travel_time_minutes=travel_time_minutes_from_length_px( length_px ) )
