from __future__ import annotations

from typing import Any

from ..core.available_schedule_slot_finder import AvailableScheduleSlotFinder
from ..core.schedule_slot_resolver import ScheduleSlotResolver
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary_builder import ItineraryBuilder
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_window_preparer import ScheduleWindowPreparer
from ....shared.duration_values import duration_minutes_to_seconds
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import ScheduleTimeKey


class ScheduleSlotTimeResolver():
   @classmethod
   def resolve(
         cls,
         conn: Connection,
         saved_itinerary: SavedItinerary,
         window: tuple[ int, int ],
         duration_seconds: int,
         *,
         start_time: ScheduleTimeKey | None,
         itinerary_context: dict[ str, Any ],
         earliest_start_seconds: int | None = None ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
      anchor_seconds, day_end_seconds = window

      if earliest_start_seconds is not None:
         anchor_seconds = max( anchor_seconds, earliest_start_seconds )

      itinerary = ItineraryBuilder.build_current( saved_itinerary, **itinerary_context )
      blockers = TimeBlockBuilder.collect_from_itinerary( itinerary )
      slot = ScheduleSlotResolver.resolve(
         blockers,
         anchor_seconds,
         duration_seconds,
         day_end_seconds,
         start_time=start_time )

      if slot is None:
         error_type = (
            ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE
            if start_time is not None
            else ItineraryErrorType.NO_AVAILABLE_SLOT )

         return None, ItinerarySaveResultBuilder.save_result(
            conn,
            error_type,
            **itinerary_context )

      return slot, None


   @classmethod
   def resolve_allowing_visit_extension(
         cls,
         conn: Connection,
         saved_itinerary: SavedItinerary,
         visit_window: tuple[ int, int ],
         duration_seconds: int,
         *,
         start_time: ScheduleTimeKey | None,
         itinerary_context: dict[ str, Any ],
         day_hours_window: tuple[ int, int ] | None = None,
         earliest_start_seconds: int | None = None,
      ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
      """Prefer the guest visit window; if full, search day hours near existing schedule."""
      slot, slot_error = cls.resolve(
         conn,
         saved_itinerary,
         visit_window,
         duration_seconds,
         start_time=start_time,
         itinerary_context=itinerary_context,
         earliest_start_seconds=earliest_start_seconds )

      if slot_error is None:
         return slot, None

      if slot_error.status not in (
            ItineraryErrorType.NO_AVAILABLE_SLOT,
            ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE ):
         return None, slot_error

      if day_hours_window is None:
         prepared_day_hours = ScheduleWindowPreparer.prepare_zoo_hours(
            conn,
            saved_itinerary,
            **itinerary_context )

         if isinstance( prepared_day_hours, ItinerarySaveResult ):
            return None, slot_error

         day_hours_window = prepared_day_hours.window

      if day_hours_window == visit_window:
         return None, slot_error

      if start_time is not None:
         return cls.resolve(
            conn,
            saved_itinerary,
            day_hours_window,
            duration_seconds,
            start_time=start_time,
            itinerary_context=itinerary_context,
            earliest_start_seconds=earliest_start_seconds )

      slot = cls._resolve_extension_slot_before_or_after_visit(
         saved_itinerary,
         visit_window=visit_window,
         day_hours_window=day_hours_window,
         duration_seconds=duration_seconds,
         itinerary_context=itinerary_context )

      if slot is None:
         return None, slot_error

      return slot, None


   @classmethod
   def _resolve_extension_slot_before_or_after_visit(
         cls,
         saved_itinerary: SavedItinerary,
         *,
         visit_window: tuple[ int, int ],
         day_hours_window: tuple[ int, int ],
         duration_seconds: int,
         itinerary_context: dict[ str, Any ],
      ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
      """After the visit window is full, try duration before arrival, then after departure."""
      itinerary = ItineraryBuilder.build_current( saved_itinerary, **itinerary_context )
      blockers = TimeBlockBuilder.collect_from_itinerary( itinerary )
      day_start_seconds, day_end_seconds = day_hours_window
      arrival_seconds, departure_seconds = visit_window

      return AvailableScheduleSlotFinder.find_before_or_after_bounds(
         blockers,
         duration_seconds,
         day_start_seconds=day_start_seconds,
         day_end_seconds=day_end_seconds,
         before_end_seconds=arrival_seconds,
         after_start_seconds=departure_seconds )


   @classmethod
   def effective_duration_seconds(
         cls,
         duration_minutes: int | None,
         default_duration_seconds: int | None ) -> int | None:
      if default_duration_seconds is None:
         return None

      if duration_minutes is not None:
         return duration_minutes_to_seconds( duration_minutes )

      return default_duration_seconds
