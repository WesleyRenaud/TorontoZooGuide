from __future__ import annotations

from .core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from .core.time_block_builder import TimeBlockBuilder
from ..data_access.itinerary_time_provider import ItineraryTimeProvider
from .items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from ...models import Itinerary
from ...shared.calendar_dates import DateValues
from ...types import Types


class ScheduledEndpointVisitTimesSyncer():
   @classmethod
   def is_fully_scheduled( cls, itinerary: Itinerary ) -> bool:
      """True when guest animals/attractions/transportations/events are all scheduled and something is on the clock.

      Guardians talks and wild encounters are fixed-time items; they do not themselves
      mark an itinerary incomplete. An empty day with no scheduled blocks is not
      considered fully scheduled.
      """
      if GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary ):
         return False

      return TimeBlockBuilder.earliest_start_seconds( itinerary ) is not None


   @classmethod
   def seed_if_complete(
         cls,
         conn: Types.Connection,
         itinerary: Itinerary ) -> None:
      """Set arrival/departure from scheduled endpoints when fully scheduled."""
      cls._apply_from_endpoints( conn, itinerary )


   @classmethod
   def sync_if_complete(
         cls,
         conn: Types.Connection,
         itinerary: Itinerary ) -> None:
      """Set arrival/departure from scheduled endpoints when fully scheduled.

      Arrival is the earliest item start minus floored walk time from the entrance
      to that item. Departure is the latest scheduled end plus floored walk time
      from that item back to the entrance. Always overwrites when the day is fully
      scheduled so callers share one derivation.
      """
      cls.seed_if_complete( conn, itinerary )


   @classmethod
   def clear_if_became_incomplete(
         cls,
         conn: Types.Connection,
         *,
         previous_itinerary: Itinerary | None,
         current_itinerary: Itinerary ) -> None:
      """Clear arrival/departure when the itinerary leaves a fully-scheduled state."""
      if previous_itinerary is None:
         return

      if not cls.is_fully_scheduled( previous_itinerary ):
         return

      if cls.is_fully_scheduled( current_itinerary ):
         return

      if DateValues.normalize_schedule_time_key( current_itinerary.arrival_time ):
         ItineraryTimeProvider.set_itinerary_arrival_time( conn, None )

      if DateValues.normalize_schedule_time_key( current_itinerary.departure_time ):
         ItineraryTimeProvider.set_itinerary_departure_time( conn, None )


   @classmethod
   def _apply_from_endpoints(
         cls,
         conn: Types.Connection,
         itinerary: Itinerary ) -> None:
      if not cls.is_fully_scheduled( itinerary ):
         return

      earliest_start_seconds = TimeBlockBuilder.earliest_start_seconds( itinerary )
      latest_end_seconds = TimeBlockBuilder.latest_end_seconds( itinerary )

      if earliest_start_seconds is None or latest_end_seconds is None:
         return

      arrival_seconds = (
         earliest_start_seconds
         - ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item( itinerary ) )
      departure_seconds = (
         latest_end_seconds
         + ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item( itinerary ) )
      arrival_time = DateValues.schedule_time_key_from_seconds( arrival_seconds )
      departure_time = DateValues.schedule_time_key_from_seconds(
         departure_seconds )

      if itinerary.arrival_time != arrival_time:
         ItineraryTimeProvider.set_itinerary_arrival_time( conn, arrival_time )

      if itinerary.departure_time != departure_time:
         ItineraryTimeProvider.set_itinerary_departure_time( conn, departure_time )
