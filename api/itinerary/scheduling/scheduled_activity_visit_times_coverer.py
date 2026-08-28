from __future__ import annotations

from typing import Any

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_time_provider import ItineraryTimeProvider
from ..domain.itinerary_builder import ItineraryBuilder
from .scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from ...shared.calendar_dates import DateValues
from ...types import Types


class ScheduledActivityVisitTimesCoverer():
   @classmethod
   def arrival_covering_starts(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         schedule_start_times: list[ Types.ScheduleTimeKey ],
      ) -> Types.ScheduleTimeKey:
      if arrival_time is None:
         return None

      covered_arrival_time = arrival_time

      for start_time in schedule_start_times:
         if DateValues.time_value_is_before( start_time, covered_arrival_time ):
            covered_arrival_time = start_time

      return covered_arrival_time


   @classmethod
   def departure_covering_ends(
         cls,
         departure_time: Types.ScheduleTimeKey,
         schedule_end_times: list[ Types.ScheduleTimeKey ],
      ) -> Types.ScheduleTimeKey:
      if departure_time is None:
         return None

      covered_departure_time = departure_time

      for end_time in schedule_end_times:
         if DateValues.time_value_is_after( end_time, covered_departure_time ):
            covered_departure_time = end_time

      return covered_departure_time


   @classmethod
   def ensure_arrival_covers_start(
         cls,
         conn: Types.Connection,
         *,
         start_time: Types.ScheduleTimeKey,
         current_arrival_time: Types.ScheduleTimeKey ) -> bool:
      if not DateValues.time_value_is_before( start_time, current_arrival_time ):
         return False

      return ItineraryTimeProvider.set_itinerary_arrival_time( conn, start_time )


   @classmethod
   def ensure_departure_covers_end(
         cls,
         conn: Types.Connection,
         *,
         end_time: Types.ScheduleTimeKey,
         current_departure_time: Types.ScheduleTimeKey ) -> bool:
      if not DateValues.time_value_is_after( end_time, current_departure_time ):
         return False

      return ItineraryTimeProvider.set_itinerary_departure_time( conn, end_time )


   @classmethod
   def cover_for_activity(
         cls,
         conn: Types.Connection,
         *,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         current_arrival_time: Types.ScheduleTimeKey,
         current_departure_time: Types.ScheduleTimeKey,
         itinerary_context: dict[ str, Any ],
         seed_if_complete: bool = True,
      ) -> None:
      """Extend arrival/departure to cover an activity; optionally seed unset visit times."""
      cls.ensure_arrival_covers_start(
         conn,
         start_time=start_time,
         current_arrival_time=current_arrival_time )
      cls.ensure_departure_covers_end(
         conn,
         end_time=end_time,
         current_departure_time=current_departure_time )

      if not seed_if_complete:
         return

      ScheduledEndpointVisitTimesSyncer.seed_if_complete(
         conn,
         ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )
