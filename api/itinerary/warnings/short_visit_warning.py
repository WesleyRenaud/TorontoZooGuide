from __future__ import annotations

from ..data_access.itinerary_status import is_itinerary_error_suppressed
from .itinerary_suppressed_warnings import append_suppressed_warning
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import Connection, ScheduleTimeKey
from ..validation.itinerary_visit_duration_validation import itinerary_visit_is_shorter_than_minimum


def short_visit_warning_is_required(
      conn: Connection,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      *,
      confirming_short_visit: bool,
      suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> bool:
   if confirming_short_visit:
      return False

   if is_itinerary_error_suppressed(
         conn,
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ):
      if suppressed_warnings is not None:
         append_suppressed_warning(
            suppressed_warnings,
            ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

      return False

   arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
   departure_minutes = DateValues.time_value_in_minutes( departure_time )

   if arrival_minutes is None or departure_minutes is None:
      return False

   return itinerary_visit_is_shorter_than_minimum(
      arrival_time,
      departure_time )
