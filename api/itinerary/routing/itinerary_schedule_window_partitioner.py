from __future__ import annotations

from .itinerary_fixed_time_stop import ItineraryFixedTimeStop
from .itinerary_fixed_time_stop_builder import ItineraryFixedTimeStopBuilder
from .itinerary_schedule_window import ItineraryScheduleWindow
from .itinerary_stop import ItineraryStop


class ItineraryScheduleWindowPartitioner():
   @classmethod
   def partition(
         cls,
         anchor_seconds: int,
         day_end_seconds: int,
         fixed_time_stops: list[ ItineraryStop ] ) -> list[ ItineraryScheduleWindow ]:
      fixed_time_entries = ItineraryFixedTimeStopBuilder.from_itinerary_stops(
         fixed_time_stops )
      fixed_time_entries.sort( key=lambda entry: entry.start_seconds )

      windows: list[ ItineraryScheduleWindow ] = []
      cursor_seconds = anchor_seconds
      previous_fixed_stop: ItineraryStop | None = None

      for fixed_time_entry in fixed_time_entries:
         if fixed_time_entry.start_seconds > cursor_seconds:
            windows.append(
               cls._window_before_fixed_time_stop(
                  cursor_seconds,
                  fixed_time_entry,
                  previous_fixed_stop=previous_fixed_stop ) )

         cursor_seconds = max( cursor_seconds, fixed_time_entry.end_seconds )
         previous_fixed_stop = fixed_time_entry.stop

      if cursor_seconds < day_end_seconds:
         windows.append(
            ItineraryScheduleWindow(
               start_seconds=cursor_seconds,
               end_seconds=day_end_seconds,
               opens_after_fixed_time_stop=previous_fixed_stop is not None,
               start_walk_node_id=(
                  None
                  if previous_fixed_stop is None
                  else previous_fixed_stop.primary_walk_node_id() ) ) )

      return windows


   @classmethod
   def _window_before_fixed_time_stop(
         cls,
         cursor_seconds: int,
         fixed_time_entry: ItineraryFixedTimeStop,
         *,
         previous_fixed_stop: ItineraryStop | None = None ) -> ItineraryScheduleWindow:
      return ItineraryScheduleWindow(
         start_seconds=cursor_seconds,
         end_seconds=fixed_time_entry.start_seconds,
         anchor_stop=fixed_time_entry.stop,
         opens_after_fixed_time_stop=previous_fixed_stop is not None,
         start_walk_node_id=(
            None
            if previous_fixed_stop is None
            else previous_fixed_stop.primary_walk_node_id() ) )
