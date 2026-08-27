from __future__ import annotations

from typing import Any

from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ....models.itinerary_event import ItineraryEvent
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import persist_itinerary_walk_route
from .schedule_itinerary_helpers import prepare_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times_allowing_visit_extension
from ..scheduled_activity_visit_times_coverer import ScheduledActivityVisitTimesCoverer
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ItineraryEventType
from ....types import Connection


def schedule_itinerary_event(
      conn: Connection,
      *,
      event_type: ItineraryEventType,
      time_options: ParsedScheduleTimeOptions,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
   prepared_window = prepare_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( prepared_window, ItinerarySaveResult ):
      return prepared_window

   if SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
         saved_itinerary,
         event_type ):
      return build_save_result(
         conn,
         ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
         **itinerary_context )

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds( conn, event_type ) )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   slot, slot_error = resolve_slot_times_allowing_visit_extension(
      conn,
      saved_itinerary,
      prepared_window.window,
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
      ScheduleItineraryItemProvider.insert_itinerary_event_schedule( cur, event )
      conn.commit()

   finally:
      cur.close()

   ScheduledActivityVisitTimesCoverer.cover_for_activity(
      conn,
      start_time=start_time_key,
      end_time=end_time,
      current_arrival_time=saved_itinerary.arrival_time,
      current_departure_time=saved_itinerary.departure_time,
      itinerary_context=itinerary_context )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
