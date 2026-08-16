from __future__ import annotations

from ...data_access.attraction_also_transportation import attraction_is_also_transportation
from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from ...transportation.default_duration_seconds import default_duration_seconds_for_transportation
from ....types import Connection


def default_duration_seconds_for_attraction_or_transportation(
      conn: Connection,
      attraction_name: str ) -> int | None:
   if attraction_is_also_transportation( conn, attraction_name ):
      return default_duration_seconds_for_transportation(
         conn,
         attraction_name )

   return fetch_attraction_default_duration_seconds( conn, attraction_name )
