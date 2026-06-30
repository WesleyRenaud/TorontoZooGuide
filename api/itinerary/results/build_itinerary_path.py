from __future__ import annotations

from ..data_access.fetch_itinerary_walk_route import fetch_itinerary_walk_route
from ..routing.itinerary_walk_route import empty_itinerary_walk_route
from ...types import Connection


def build_itinerary_path( conn: Connection | None ) -> dict[ str, object ]:
   if conn is None:
      return empty_itinerary_walk_route().to_dict()

   return fetch_itinerary_walk_route( conn ).to_dict()
