from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .itinerary_fixed_time_stop import itinerary_fixed_time_stops_from_itinerary_stops
from .itinerary_fixed_time_stop import ItineraryFixedTimeStop
from .itinerary_stop import ItineraryStop
from .loop_schedule_pin import LoopSchedulePin


@dataclass( frozen=True )
class ItineraryScheduleWindow:
   start_seconds: int
   end_seconds: int
   anchor_stop: ItineraryStop | None = None
   loop_pins: list[ LoopSchedulePin ] = field( default_factory=list )
   opens_after_fixed_time_stop: bool = False
   start_walk_node_id: str | None = None


def partition_itinerary_schedule_windows(
      anchor_seconds: int,
      day_end_seconds: int,
      fixed_time_stops: list[ ItineraryStop ] ) -> list[ ItineraryScheduleWindow ]:
   fixed_time_entries = itinerary_fixed_time_stops_from_itinerary_stops(
      fixed_time_stops )
   fixed_time_entries.sort( key=lambda entry: entry.start_seconds )

   windows: list[ ItineraryScheduleWindow ] = []
   cursor_seconds = anchor_seconds
   previous_fixed_stop: ItineraryStop | None = None

   for fixed_time_entry in fixed_time_entries:
      if fixed_time_entry.start_seconds > cursor_seconds:
         windows.append(
            _schedule_window_before_fixed_time_stop(
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


def _schedule_window_before_fixed_time_stop(
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
