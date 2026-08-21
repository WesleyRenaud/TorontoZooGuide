from __future__ import annotations

from datetime import date

from ...models.itinerary_transportation import ItineraryTransportation
from ...request_connection import get_connection
from ...transportation.data_access.transportation_route_leg_marker import fetch_transportation_route_leg_marker_ids
from ..transportation.resolve_transportation_day_loop import resolve_transportation_route_for_date


def attach_itinerary_transportation_route_markers(
      transportations: list[ ItineraryTransportation ],
      *,
      target_date: date,
) -> None:
   conn = get_connection()

   for transportation in transportations:
      if not transportation.legs:
         continue

      route = resolve_transportation_route_for_date(
         conn,
         transportation=transportation.name,
         target_date=target_date,
      )
      transportation.route = route
      transportation.route_markers = fetch_transportation_route_leg_marker_ids(
         conn,
         transportation=transportation.name,
         route=route,
         legs=transportation.legs,
      )
