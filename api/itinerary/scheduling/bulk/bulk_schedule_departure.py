from __future__ import annotations

from ..core.time_block import latest_scheduled_end_seconds
from ...data_access.itinerary_time import set_itinerary_departure_time
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import Connection


def ensure_departure_after_bulk_schedule(
      conn: Connection,
      itinerary: Itinerary ) -> None:
   latest_end_seconds = latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return

   set_itinerary_departure_time(
      conn,
      DateValues.schedule_time_key_from_seconds( latest_end_seconds ) )
