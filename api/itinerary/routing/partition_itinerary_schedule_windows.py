from __future__ import annotations

from dataclasses import dataclass

from .itinerary_stop import ItineraryStop
from ..scheduling.core.time_block import time_block_from_schedule_times
from ..scheduling.core.time_block import TimeBlock


@dataclass( frozen=True )
class ItineraryScheduleWindow:
   start_seconds: int
   end_seconds: int


def partition_itinerary_schedule_windows(
      anchor_seconds: int,
      day_end_seconds: int,
      fixed_time_stops: list[ ItineraryStop ] ) -> list[ ItineraryScheduleWindow ]:
   fixed_blocks = _fixed_time_blocks_from_stops( fixed_time_stops )
   fixed_blocks.sort( key=lambda block: block.start_seconds )

   windows: list[ ItineraryScheduleWindow ] = []
   cursor_seconds = anchor_seconds

   for fixed_block in fixed_blocks:
      if fixed_block.start_seconds > cursor_seconds:
         windows.append(
            ItineraryScheduleWindow(
               start_seconds=cursor_seconds,
               end_seconds=fixed_block.start_seconds ) )

      cursor_seconds = max( cursor_seconds, fixed_block.end_seconds )

   if cursor_seconds < day_end_seconds:
      windows.append(
         ItineraryScheduleWindow(
            start_seconds=cursor_seconds,
            end_seconds=day_end_seconds ) )

   return windows


def _fixed_time_blocks_from_stops(
      fixed_time_stops: list[ ItineraryStop ] ) -> list[ TimeBlock ]:
   blocks: list[ TimeBlock ] = []

   for stop in fixed_time_stops:
      block = time_block_from_schedule_times(
         stop.start_time,
         stop.end_time )

      if block is not None:
         blocks.append( block )

   return blocks
