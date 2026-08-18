from __future__ import annotations

from .core.guest_item_schedule_status import itinerary_has_unscheduled_guest_items
from .core.time_block import earliest_scheduled_start_seconds
from .core.time_block import latest_scheduled_end_seconds
from ..data_access.itinerary_time import set_itinerary_arrival_time
from ..data_access.itinerary_time import set_itinerary_departure_time
from .items.schedule_item_travel_time import entrance_travel_seconds_from_latest_item
from .items.schedule_item_travel_time import entrance_travel_seconds_to_earliest_item
from ...models import Itinerary
from ...shared.calendar_dates import DateValues
from ...types import Connection


def itinerary_is_fully_scheduled( itinerary: Itinerary ) -> bool:
   """True when guest animals/attractions/transportations/events are all scheduled and something is on the clock.

   Guardians talks and wild encounters are fixed-time items; they do not themselves
   mark an itinerary incomplete. An empty day with no scheduled blocks is not
   considered fully scheduled.
   """
   if itinerary_has_unscheduled_guest_items( itinerary ):
      return False

   return earliest_scheduled_start_seconds( itinerary ) is not None


def seed_visit_times_to_scheduled_endpoints_if_complete(
      conn: Connection,
      itinerary: Itinerary ) -> None:
   """Set arrival/departure from scheduled endpoints when fully scheduled."""
   _apply_visit_times_from_scheduled_endpoints( conn, itinerary )


def sync_visit_times_to_scheduled_endpoints_if_complete(
      conn: Connection,
      itinerary: Itinerary ) -> None:
   """Set arrival/departure from scheduled endpoints when fully scheduled.

   Arrival is the earliest item start minus floored walk time from the entrance
   to that item. Departure is the latest scheduled end plus floored walk time
   from that item back to the entrance. Always overwrites when the day is fully
   scheduled so callers share one derivation.
   """
   seed_visit_times_to_scheduled_endpoints_if_complete( conn, itinerary )


def clear_visit_times_if_became_incomplete(
      conn: Connection,
      *,
      previous_itinerary: Itinerary | None,
      current_itinerary: Itinerary ) -> None:
   """Clear arrival/departure when the itinerary leaves a fully-scheduled state."""
   if previous_itinerary is None:
      return

   if not itinerary_is_fully_scheduled( previous_itinerary ):
      return

   if itinerary_is_fully_scheduled( current_itinerary ):
      return

   if DateValues.normalize_schedule_time_key( current_itinerary.arrival_time ):
      set_itinerary_arrival_time( conn, None )

   if DateValues.normalize_schedule_time_key( current_itinerary.departure_time ):
      set_itinerary_departure_time( conn, None )


def _apply_visit_times_from_scheduled_endpoints(
      conn: Connection,
      itinerary: Itinerary ) -> None:
   if not itinerary_is_fully_scheduled( itinerary ):
      return

   earliest_start_seconds = earliest_scheduled_start_seconds( itinerary )
   latest_end_seconds = latest_scheduled_end_seconds( itinerary )

   if earliest_start_seconds is None or latest_end_seconds is None:
      return

   arrival_seconds = (
      earliest_start_seconds
      - entrance_travel_seconds_to_earliest_item( itinerary ) )
   departure_seconds = (
      latest_end_seconds
      + entrance_travel_seconds_from_latest_item( itinerary ) )
   arrival_time = DateValues.schedule_time_key_from_seconds( arrival_seconds )
   departure_time = DateValues.schedule_time_key_from_seconds(
      departure_seconds )

   if itinerary.arrival_time != arrival_time:
      set_itinerary_arrival_time( conn, arrival_time )

   if itinerary.departure_time != departure_time:
      set_itinerary_departure_time( conn, departure_time )
