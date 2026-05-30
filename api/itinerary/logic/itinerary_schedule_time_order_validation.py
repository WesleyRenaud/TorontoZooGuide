from __future__ import annotations

from ...shared.date_values import DateValues
from ...types import ScheduleTimeKey


def departure_follows_arrival(
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   return DateValues.time_value_in_minutes( departure_time ) > DateValues.time_value_in_minutes(
      arrival_time )
