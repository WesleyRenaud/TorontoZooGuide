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
      visit_duration_minutes = (
         DateValues.time_value_in_minutes( departure_time )
         - DateValues.time_value_in_minutes( arrival_time )
      )

      return visit_duration_minutes < Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES
