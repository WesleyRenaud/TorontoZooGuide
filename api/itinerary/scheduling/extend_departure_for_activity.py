from __future__ import annotations

from typing import Any

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_time_provider import ItineraryTimeProvider
from ..domain.itinerary_builder import ItineraryBuilder
from ...shared.calendar_dates import DateValues
from .sync_visit_times_to_scheduled_endpoints import seed_visit_times_to_scheduled_endpoints_if_complete
from ...types import Connection
from ...types import ScheduleTimeKey


def arrival_time_covering_schedule_starts(
      arrival_time: ScheduleTimeKey,
      schedule_start_times: list[ ScheduleTimeKey ],
   ) -> ScheduleTimeKey:
   if arrival_time is None:
      return None

   covered_arrival_time = arrival_time

   for start_time in schedule_start_times:
      if DateValues.time_value_is_before( start_time, covered_arrival_time ):
         covered_arrival_time = start_time

   return covered_arrival_time


def departure_time_covering_schedule_ends(
      departure_time: ScheduleTimeKey,
      schedule_end_times: list[ ScheduleTimeKey ],
   ) -> ScheduleTimeKey:
   if departure_time is None:
      return None

   covered_departure_time = departure_time

   for end_time in schedule_end_times:
      if DateValues.time_value_is_after( end_time, covered_departure_time ):
         covered_departure_time = end_time

   return covered_departure_time


def ensure_arrival_covers_start_time(
      conn: Connection,
      *,
      start_time: ScheduleTimeKey,
      current_arrival_time: ScheduleTimeKey ) -> bool:
   if not DateValues.time_value_is_before( start_time, current_arrival_time ):
      return False

   return ItineraryTimeProvider.set_itinerary_arrival_time( conn, start_time )


def ensure_departure_covers_end_time(
      conn: Connection,
      *,
      end_time: ScheduleTimeKey,
      current_departure_time: ScheduleTimeKey ) -> bool:
   if not DateValues.time_value_is_after( end_time, current_departure_time ):
      return False

   return ItineraryTimeProvider.set_itinerary_departure_time( conn, end_time )


def cover_visit_times_for_scheduled_activity(
      conn: Connection,
      *,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      current_arrival_time: ScheduleTimeKey,
      current_departure_time: ScheduleTimeKey,
      itinerary_context: dict[ str, Any ],
      seed_if_complete: bool = True,
   ) -> None:
   """Extend arrival/departure to cover an activity; optionally seed unset visit times."""
   ensure_arrival_covers_start_time(
      conn,
      start_time=start_time,
      current_arrival_time=current_arrival_time )
   ensure_departure_covers_end_time(
      conn,
      end_time=end_time,
      current_departure_time=current_departure_time )

   if not seed_if_complete:
      return

   seed_visit_times_to_scheduled_endpoints_if_complete(
      conn,
      ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )
