from __future__ import annotations

from ..data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ..routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from ...types import Connection


def build_itinerary_path( conn: Connection | None ) -> dict[ str, object ]:
   if conn is None:
      return ItineraryWalkRouteBuilder.empty().to_dict()

   return ItineraryWalkRouteProvider.fetch_itinerary_walk_route( conn ).to_dict()
