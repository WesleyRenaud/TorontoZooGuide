from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind
from .transit_ride_endpoint import TransitRideEndpoint
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class WalkRouteAnchor:
   schedule_item_kind: ScheduleItemKind
   item_key: str
   walk_node_ids: list[ str ]
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None
   # Onboarding/offboarding pair for one transportation ride sequence.
   transit_ride_key: str | None = None
   transit_endpoint: TransitRideEndpoint | None = None
