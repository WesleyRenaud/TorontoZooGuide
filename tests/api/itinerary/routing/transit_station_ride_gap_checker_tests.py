from __future__ import annotations

from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transit_station_ride_gap_checker import TransitStationRideGapChecker
from api.itinerary.routing.walk_route_anchor import WalkRouteAnchor
from api.shared.enums import ScheduleItemKind


ONBOARDING_ANCHOR = WalkRouteAnchor(
   schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
   item_key='Zoomobile||Main Zoomobile Station',
   walk_node_ids=[ 'n-100' ],
   transit_ride_key='ride-1',
   transit_endpoint=TransitRideEndpoint.ONBOARDING,
)

OFFBOARDING_ANCHOR = WalkRouteAnchor(
   schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
   item_key='Zoomobile||Canadian Domain Zoomobile Station',
   walk_node_ids=[ 'n-200' ],
   transit_ride_key='ride-1',
   transit_endpoint=TransitRideEndpoint.OFFBOARDING,
)

OTHER_RIDE_OFFBOARDING_ANCHOR = WalkRouteAnchor(
   schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
   item_key='Zoomobile||Africa Zoomobile Station',
   walk_node_ids=[ 'n-300' ],
   transit_ride_key='ride-2',
   transit_endpoint=TransitRideEndpoint.OFFBOARDING,
)


def Test_IsGap_TestOnboardThenOffboardSameRide_ExpectTrue() -> None:
   assert TransitStationRideGapChecker.is_gap(
      ONBOARDING_ANCHOR,
      OFFBOARDING_ANCHOR )


def Test_IsGap_TestOffboardThenOnboard_ExpectFalse() -> None:
   assert not TransitStationRideGapChecker.is_gap(
      OFFBOARDING_ANCHOR,
      ONBOARDING_ANCHOR )


def Test_IsGap_TestDifferentRideKeys_ExpectFalse() -> None:
   assert not TransitStationRideGapChecker.is_gap(
      ONBOARDING_ANCHOR,
      OTHER_RIDE_OFFBOARDING_ANCHOR )
