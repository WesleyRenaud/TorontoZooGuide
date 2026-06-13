from __future__ import annotations

from dataclasses import dataclass

from ...shared.calendar_dates import DateValues
from ...shared.duration_values import normalize_duration_minutes
from ...shared.enums import ItineraryErrorType
from ...types import DurationInput
from ...types import ScheduleTimeKey
from ...types import TimeInput


@dataclass( frozen=True )
class ParsedScheduleTimeOptions:
   start_time: ScheduleTimeKey
   duration_minutes: int | None

   def to_dict( self ) -> dict[ str, ScheduleTimeKey | int | None ]:
      return {
         'start_time': self.start_time,
         'duration_minutes': self.duration_minutes,
      }


def parse_schedule_time_options(
      start_time: TimeInput,
      duration_minutes: DurationInput ) -> ParsedScheduleTimeOptions | ItineraryErrorType:
   start_time_was_provided = bool(
      DateValues.normalize_schedule_time_key( start_time ) )
   normalized_start = DateValues.normalize_itinerary_schedule_time( start_time )

   if start_time_was_provided and normalized_start is None:
      return ItineraryErrorType.SAVE_FAILED

   parsed_duration = normalize_duration_minutes( duration_minutes )

   if duration_minutes is not None and parsed_duration is None:
      return ItineraryErrorType.SAVE_FAILED

   if parsed_duration is not None and normalized_start is None:
      return ItineraryErrorType.SAVE_FAILED

   return ParsedScheduleTimeOptions(
      start_time=normalized_start,
      duration_minutes=parsed_duration,
   )
