from __future__ import annotations

from ..core.time_block import earliest_scheduled_start_seconds
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ...domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from ...domain.itinerary_adjustment_type import ItineraryAdjustmentType
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import Connection


def adjust_arrival_after_bulk_schedule(
      conn: Connection,
      itinerary: Itinerary,
      *,
      schedule_anchor_seconds: int,
      previous_arrival_time: str | None ) -> ItineraryAdjustment | None:
   earliest_start_seconds = earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return None

   previous_arrival_seconds = DateValues.time_value_in_seconds(
      previous_arrival_time )

   if not _should_sync_arrival_to_earliest_item(
         earliest_start_seconds=earliest_start_seconds,
         schedule_anchor_seconds=schedule_anchor_seconds,
         previous_arrival_seconds=previous_arrival_seconds ):
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
      reason=ItineraryAdjustmentReason.BULK_SCHEDULE_CONSECUTIVE_PACKING )


def _should_sync_arrival_to_earliest_item(
      *,
      earliest_start_seconds: int,
      schedule_anchor_seconds: int,
      previous_arrival_seconds: int | None ) -> bool:
   if previous_arrival_seconds is None:
      return earliest_start_seconds > schedule_anchor_seconds

   if previous_arrival_seconds > earliest_start_seconds:
      return True

   return (
      earliest_start_seconds > schedule_anchor_seconds
      and earliest_start_seconds > previous_arrival_seconds )
