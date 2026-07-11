from __future__ import annotations

from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary_time import set_itinerary_departure_time
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import Connection


def ensure_departure_after_bulk_schedule(
      conn: Connection,
      itinerary: Itinerary ) -> None:
   time_blocks = collect_time_blocks_from_itinerary( itinerary )

   if not time_blocks:
      return

   latest_end_seconds = max(
      time_block.end_seconds for time_block in time_blocks )

   set_itinerary_departure_time(
      conn,
      DateValues.schedule_time_key_from_seconds( latest_end_seconds ) )
