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
      """Fill unset arrival/departure from scheduled endpoints when fully scheduled.

      Times the guest already set are left alone.
      """
      if not cls._has_endpoints( itinerary ):
         return

      if not DateValues.normalize_schedule_time_key( itinerary.arrival_time ):
         ItineraryTimeProvider.set_itinerary_arrival_time(
            conn,
            cls._endpoint_arrival_time( itinerary ) )

      if not DateValues.normalize_schedule_time_key( itinerary.departure_time ):
         ItineraryTimeProvider.set_itinerary_departure_time(
            conn,
            cls._endpoint_departure_time( itinerary ) )


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
      if not cls._has_endpoints( itinerary ):
         return

      arrival_time = cls._endpoint_arrival_time( itinerary )
      departure_time = cls._endpoint_departure_time( itinerary )

      if itinerary.arrival_time != arrival_time:
         ItineraryTimeProvider.set_itinerary_arrival_time( conn, arrival_time )

      if itinerary.departure_time != departure_time:
         ItineraryTimeProvider.set_itinerary_departure_time( conn, departure_time )


   @classmethod
   def clear_if_became_incomplete(
         cls,
         conn: Types.Connection,
         *,
         previous_itinerary: Itinerary | None,
         current_itinerary: Itinerary ) -> None:
      """Clear arrival/departure when a fully-scheduled itinerary gains unscheduled guest items.

      An itinerary left with nothing on it keeps the guest's times.
      """
      if previous_itinerary is None:
         return

      if not cls.is_fully_scheduled( previous_itinerary ):
         return

      if not GuestItemScheduleStatusChecker.has_unscheduled_guest_items( current_itinerary ):
         return

      if DateValues.normalize_schedule_time_key( current_itinerary.arrival_time ):
         ItineraryTimeProvider.set_itinerary_arrival_time( conn, None )

      if DateValues.normalize_schedule_time_key( current_itinerary.departure_time ):
         ItineraryTimeProvider.set_itinerary_departure_time( conn, None )


   @classmethod
   def _has_endpoints( cls, itinerary: Itinerary ) -> bool:
      if not cls.is_fully_scheduled( itinerary ):
         return False

      return TimeBlockBuilder.latest_end_seconds( itinerary ) is not None


   @classmethod
   def _endpoint_arrival_time( cls, itinerary: Itinerary ) -> Types.ScheduleTimeKey:
      return DateValues.schedule_time_key_from_seconds(
         TimeBlockBuilder.earliest_start_seconds( itinerary )
         - ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item( itinerary ) )


   @classmethod
   def _endpoint_departure_time( cls, itinerary: Itinerary ) -> Types.ScheduleTimeKey:
      return DateValues.schedule_time_key_from_seconds(
         TimeBlockBuilder.latest_end_seconds( itinerary )
         + ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item( itinerary ) )
