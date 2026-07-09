from __future__ import annotations

from ...data_access.itinerary import fetch_itinerary_animal_rows
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ...domain.itinerary_adjustment import ItineraryAdjustmentType
from ....shared.calendar_dates import DateValues
from ....types import Connection


def adjust_arrival_after_bulk_schedule(
      conn: Connection,
      *,
      schedule_anchor_seconds: int,
      previous_arrival_time: str | None ) -> ItineraryAdjustment | None:
   earliest_start_seconds = _earliest_scheduled_animal_start_seconds( conn )

   if (
         earliest_start_seconds is None
         or earliest_start_seconds <= schedule_anchor_seconds ):
      return None

   adjusted_arrival_time = DateValues.schedule_time_key_from_seconds(
      earliest_start_seconds )

   if (
         previous_arrival_time is not None
         and adjusted_arrival_time == previous_arrival_time ):
      return None

   set_itinerary_arrival_time( conn, adjusted_arrival_time )

   return ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=previous_arrival_time,
      value=adjusted_arrival_time,
      reason='bulkScheduleConsecutivePacking' )


def _earliest_scheduled_animal_start_seconds(
      conn: Connection ) -> int | None:
   earliest_start_seconds: int | None = None

   for animal_row in fetch_itinerary_animal_rows( conn ):
      start_seconds = DateValues.time_value_in_seconds( animal_row.start_time )

      if start_seconds is None:
         continue

      if (
            earliest_start_seconds is None
            or start_seconds < earliest_start_seconds ):
         earliest_start_seconds = start_seconds

   return earliest_start_seconds
