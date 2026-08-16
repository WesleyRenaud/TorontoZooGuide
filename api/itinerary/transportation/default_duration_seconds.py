from __future__ import annotations

from ..data_access.itinerary import fetch_itinerary_date
from .resolve_transportation_day_loop import fetch_transportation_day_loop
from ...shared.calendar_dates import DateValues
from ...types import Connection


def default_duration_seconds_for_transportation(
      conn: Connection,
      transportation: str ) -> int | None:
   visit_date = fetch_itinerary_date( conn )
   parsed_visit_date = DateValues.parse_date_value( visit_date )

   if parsed_visit_date is None:
      return None

   day_loop = fetch_transportation_day_loop(
      conn,
      transportation=transportation,
      target_date=parsed_visit_date )

   if day_loop is None:
      return None

   return day_loop.duration_seconds()
