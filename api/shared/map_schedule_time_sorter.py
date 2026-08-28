from __future__ import annotations

from .calendar_dates import DateValues
from ..types import Types


class MapScheduleTimeSorter():
   @classmethod
   def unique_sorted(
         cls,
         times: list[ Types.ScheduleTimeKey ] ) -> list[ str ]:
      unique_times: dict[ int, str ] = {}

      for time_value in times:
         normalized_time = DateValues.normalize_schedule_time( time_value )

         if not normalized_time:
            continue

         time_seconds = DateValues.time_value_in_seconds( normalized_time )

         if time_seconds is None:
            continue

         unique_times.setdefault( time_seconds, normalized_time )

      return [
         unique_times[ time_seconds ]
         for time_seconds in sorted( unique_times )
      ]
