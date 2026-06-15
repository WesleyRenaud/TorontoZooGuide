from __future__ import annotations

from typing import Any

from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_default_duration import fetch_event_default_duration_seconds
from ...data_access.schedule_itinerary_item import insert_itinerary_event_schedule
from ....models.itinerary_event import ItineraryEvent
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import resolve_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ItineraryEventType
from ....types import Connection


def schedule_itinerary_event(
      conn: Connection,
      *,
      event_type: ItineraryEventType,
      time_options: ParsedScheduleTimeOptions,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   window = resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( window, ItinerarySaveResult ):
      return window

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      fetch_event_default_duration_seconds( conn, event_type ) )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   slot, slot_error = resolve_slot_times(
      conn,
      saved_itinerary,
      window,
      duration_seconds,
      start_time=time_options.start_time,
      itinerary_context=itinerary_context )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot
   event = ItineraryEvent(
      event_type=event_type,
      start_time=start_time_key,
      end_time=end_time )

   cur = conn.cursor()

   try:
      insert_itinerary_event_schedule( cur, event )
      conn.commit()

   finally:
      cur.close()

   return build_success_result( conn, **itinerary_context )
