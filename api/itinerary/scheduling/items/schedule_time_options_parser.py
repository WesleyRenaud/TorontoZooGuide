from __future__ import annotations

from .parsed_schedule_time_options import ParsedScheduleTimeOptions
from ....shared.calendar_dates import DateValues
from ....shared.duration_values import DurationValues
from ....shared.enums import ItineraryErrorType
from ....types import DurationInput
from ....types import TimeInput


class ScheduleTimeOptionsParser():
   @classmethod
   def parse(
         cls,
         start_time: TimeInput,
         duration_minutes: DurationInput ) -> ParsedScheduleTimeOptions | ItineraryErrorType:
      start_time_was_provided = bool(
         DateValues.normalize_schedule_time_key( start_time ) )
      normalized_start = DateValues.normalize_itinerary_schedule_time( start_time )

      if start_time_was_provided and normalized_start is None:
         return ItineraryErrorType.SAVE_FAILED

      parsed_duration = DurationValues.normalize_minutes( duration_minutes )

      if duration_minutes is not None and parsed_duration is None:
         return ItineraryErrorType.SAVE_FAILED

      return ParsedScheduleTimeOptions(
         start_time=normalized_start,
         duration_minutes=parsed_duration,
      )
