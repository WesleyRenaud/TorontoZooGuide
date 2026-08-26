from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...types import ScheduleTimeKey


class ItineraryScheduleTimeOrderValidationBuilder():
   @classmethod
   def departure_follows_arrival(
         cls,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey ) -> bool:
      arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
      departure_minutes = DateValues.time_value_in_minutes( departure_time )

      if arrival_minutes is None or departure_minutes is None:
         return True

      return departure_minutes > arrival_minutes
