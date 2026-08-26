from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...shared.constants import MIN_ITINERARY_VISIT_DURATION_MINUTES
from ...types import ScheduleTimeKey


class ItineraryVisitDurationValidationBuilder():
   @classmethod
   def is_shorter_than_minimum(
         cls,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey ) -> bool:
      visit_duration_minutes = (
         DateValues.time_value_in_minutes( departure_time )
         - DateValues.time_value_in_minutes( arrival_time )
      )

      return visit_duration_minutes < MIN_ITINERARY_VISIT_DURATION_MINUTES
