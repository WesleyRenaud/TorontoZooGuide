from __future__ import annotations

from ..data_access.itinerary_error_suppression import is_itinerary_error_suppressed
from ..data_access.itinerary_error_suppression import suppress_itinerary_error
from .itinerary_visit_duration_validation import itinerary_visit_is_shorter_than_minimum
from ...shared.enums import ItineraryErrorType
from ...types import Connection, ScheduleTimeKey


def short_visit_warning_is_required(
      conn: Connection,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      *,
      confirming_short_visit: bool ) -> bool:
   if confirming_short_visit:
      return False

   if is_itinerary_error_suppressed(
         conn,
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ):
      return False

   return itinerary_visit_is_shorter_than_minimum(
      arrival_time,
      departure_time )


def apply_short_visit_warning_preferences(
      conn: Connection,
      *,
      suppress_short_visit_warning: bool ) -> None:
   if not suppress_short_visit_warning:
      return

   suppress_itinerary_error(
      conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
