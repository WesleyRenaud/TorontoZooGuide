from __future__ import annotations

from datetime import date

from .resolve_transportation_day_loop import fetch_transportation_day_loop
from ...types import Connection


def transportation_route_duration_minutes(
      conn: Connection,
      *,
      transportation: str,
      target_date: date,
) -> int | None:
   day_loop = fetch_transportation_day_loop(
      conn,
      transportation=transportation,
      target_date=target_date,
   )

   if day_loop is None:
      return None

   return day_loop.duration_minutes()
