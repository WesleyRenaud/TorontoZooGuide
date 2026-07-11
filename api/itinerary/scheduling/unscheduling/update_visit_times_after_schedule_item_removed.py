from __future__ import annotations

from ..core.time_block import collect_time_blocks_from_itinerary
from ..core.time_block import TimeBlock
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...data_access.itinerary_time import set_itinerary_departure_time
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ...domain.itinerary_adjustment import ItineraryAdjustmentType
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import Connection


def was_first_scheduled_item(
      itinerary: Itinerary,
      removed_block: TimeBlock | None ) -> bool:
   if removed_block is None:
      return False

   earliest_start_seconds = _earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return False

   return removed_block.start_seconds == earliest_start_seconds


def was_last_scheduled_item(
      itinerary: Itinerary,
      removed_block: TimeBlock | None ) -> bool:
   if removed_block is None:
      return False

   latest_end_seconds = _latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return False

   return removed_block.end_seconds == latest_end_seconds


def update_arrival_to_earliest_scheduled_start(
      conn: Connection,
      itinerary: Itinerary,
      *,
      previous_arrival_time: str | None ) -> ItineraryAdjustment | None:
   earliest_start_seconds = _earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return None

   adjusted_arrival_time = DateValues.schedule_time_key_from_seconds(
      earliest_start_seconds )

   if adjusted_arrival_time == previous_arrival_time:
      return None

   set_itinerary_arrival_time( conn, adjusted_arrival_time )

   return ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=previous_arrival_time,
      value=adjusted_arrival_time,
      reason='scheduleItemRemoved' )


def update_departure_to_latest_scheduled_end(
      conn: Connection,
      itinerary: Itinerary,
      *,
      previous_departure_time: str | None ) -> ItineraryAdjustment | None:
   latest_end_seconds = _latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return None

   adjusted_departure_time = DateValues.schedule_time_key_from_seconds(
      latest_end_seconds )

   if adjusted_departure_time == previous_departure_time:
      return None

   set_itinerary_departure_time( conn, adjusted_departure_time )

   return ItineraryAdjustment(
      type=ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED,
      field='departureTime',
      previous_value=previous_departure_time,
      value=adjusted_departure_time,
      reason='scheduleItemRemoved' )


def _earliest_scheduled_start_seconds( itinerary: Itinerary ) -> int | None:
   time_blocks = collect_time_blocks_from_itinerary( itinerary )

   if not time_blocks:
      return None

   return min( time_block.start_seconds for time_block in time_blocks )


def _latest_scheduled_end_seconds( itinerary: Itinerary ) -> int | None:
   time_blocks = collect_time_blocks_from_itinerary( itinerary )

   if not time_blocks:
      return None

   return max( time_block.end_seconds for time_block in time_blocks )
