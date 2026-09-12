from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...shared.constants import Constants
from ...types import Types


class ItineraryVisitDurationValidator():
   @classmethod
   def is_shorter_than_minimum(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey ) -> bool:
      arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
      departure_minutes = DateValues.time_value_in_minutes( departure_time )

      if arrival_minutes is None or departure_minutes is None:
         return False

      return (
         departure_minutes - arrival_minutes
         < Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES
      )
