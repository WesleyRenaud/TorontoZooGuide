from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...shared.constants import MIN_ITINERARY_VISIT_DURATION_MINUTES
from ...types import ScheduleTimeKey


def itinerary_visit_is_shorter_than_minimum(
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   visit_duration_minutes = (
      DateValues.time_value_in_minutes( departure_time )
      - DateValues.time_value_in_minutes( arrival_time )
   )

   return visit_duration_minutes < MIN_ITINERARY_VISIT_DURATION_MINUTES
