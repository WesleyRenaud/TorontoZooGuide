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


def is_transit_station_ride_gap(
      previous: WalkRouteAnchor,
      current: WalkRouteAnchor,
) -> bool:
   """True when the gap is covered by a ride, not a walk."""
   return (
      previous.transit_ride_key is not None
      and previous.transit_ride_key == current.transit_ride_key
      and previous.transit_endpoint is TransitRideEndpoint.ONBOARDING
      and current.transit_endpoint is TransitRideEndpoint.OFFBOARDING
   )
