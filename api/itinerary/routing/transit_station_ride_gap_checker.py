from __future__ import annotations

from .transit_ride_endpoint import TransitRideEndpoint
from .walk_route_anchor import WalkRouteAnchor


class TransitStationRideGapChecker():
   @classmethod
   def is_gap(
         cls,
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
