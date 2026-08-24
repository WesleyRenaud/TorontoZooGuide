from __future__ import annotations

from dataclasses import dataclass

from .calendar_dates import DateValues
from ..types import ScheduleTimeKey


@dataclass( frozen=True )
class OperatingHours:
   open_seconds: int
   close_seconds: int

   @classmethod
   def from_schedule_times(
         cls,
         open_time: ScheduleTimeKey,
         close_time: ScheduleTimeKey,
   ) -> OperatingHours | None:
      open_seconds = DateValues.time_value_in_seconds( open_time )
      close_seconds = DateValues.time_value_in_seconds( close_time )

      if open_seconds is None or close_seconds is None:
         return None

      return cls(
         open_seconds=open_seconds,
         close_seconds=close_seconds )
