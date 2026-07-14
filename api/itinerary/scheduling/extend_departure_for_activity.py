from __future__ import annotations

from collections.abc import Iterable

from ..data_access.itinerary_time import set_itinerary_arrival_time
from ..data_access.itinerary_time import set_itinerary_departure_time
from ...shared.calendar_dates import DateValues
from ...types import Connection
from ...types import ScheduleTimeKey


def arrival_time_covering_schedule_starts(
      arrival_time: ScheduleTimeKey,
      schedule_start_times: Iterable[ ScheduleTimeKey ],
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
      schedule_end_times: Iterable[ ScheduleTimeKey ],
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

   return set_itinerary_arrival_time( conn, start_time )


def ensure_departure_covers_end_time(
      conn: Connection,
      *,
      end_time: ScheduleTimeKey,
      current_departure_time: ScheduleTimeKey ) -> bool:
   if not DateValues.time_value_is_after( end_time, current_departure_time ):
      return False

   return set_itinerary_departure_time( conn, end_time )
