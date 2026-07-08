from __future__ import annotations

from dataclasses import dataclass

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import ScheduleTimeKey

LoopScheduleSlot = tuple[
   ItineraryAnimalRecord,
   ScheduleTimeKey,
   ScheduleTimeKey,
]


@dataclass( frozen=True )
class LoopGroupWindowMatch:
   window_index: int
   start_seconds: int
   schedule_window: ItineraryScheduleWindow


def schedule_animals_by_master_route_loop(
      conn: Connection,
      loop_groups: list[ list[ ItineraryAnimalRecord ] ],
      *,
      blockers: list[ TimeBlock ],
      schedule_windows: list[ ItineraryScheduleWindow ],
      schedule_cursor_seconds: int ) -> tuple[ list[ ItineraryAnimalRecord ], int ]:
   remaining_animals: list[ ItineraryAnimalRecord ] = []
   cursor_seconds = schedule_cursor_seconds
   window_index = 0

   for loop_group in loop_groups:
      unscheduled, cursor_seconds, window_index = _schedule_loop_group(
         conn,
         loop_group,
         blockers=blockers,
         schedule_windows=schedule_windows,
         cursor_seconds=cursor_seconds,
         window_index=window_index )

      remaining_animals.extend( unscheduled )

   return remaining_animals, cursor_seconds


def _schedule_loop_group(
      conn: Connection,
      animals: list[ ItineraryAnimalRecord ],
      *,
      blockers: list[ TimeBlock ],
      schedule_windows: list[ ItineraryScheduleWindow ],
      cursor_seconds: int,
      window_index: int ) -> tuple[ list[ ItineraryAnimalRecord ], int, int ]:
   durations = _fetch_viewing_durations( conn, animals )

   if durations is None:
      return animals, cursor_seconds, window_index

   window_match = _find_window_for_loop_group(
      schedule_windows,
      cursor_seconds=cursor_seconds,
      window_index=window_index,
      total_duration_seconds=sum( durations ) )

   if window_match is None:
      return animals, cursor_seconds, window_index

   animal_slots, end_seconds = _assign_contiguous_slots(
      animals,
      durations,
      start_seconds=window_match.start_seconds )

   if not _save_loop_slots( conn, blockers, animal_slots ):
      return animals, cursor_seconds, window_index

   return (
      [],
      end_seconds,
      _window_index_after_schedule(
         window_match,
         end_seconds=end_seconds ),
   )


def _find_window_for_loop_group(
      schedule_windows: list[ ItineraryScheduleWindow ],
      *,
      cursor_seconds: int,
      window_index: int,
      total_duration_seconds: int ) -> LoopGroupWindowMatch | None:
   for index in range( window_index, len( schedule_windows ) ):
      schedule_window = schedule_windows[ index ]

      if _cursor_has_passed_window( cursor_seconds, schedule_window ):
         continue

      start_seconds = _aligned_window_start_seconds(
         schedule_window,
         cursor_seconds )

      if not _loop_group_fits_in_window(
            schedule_window,
            start_seconds=start_seconds,
            total_duration_seconds=total_duration_seconds ):
         continue

      return LoopGroupWindowMatch(
         window_index=index,
         start_seconds=start_seconds,
         schedule_window=schedule_window )

   return None


def _cursor_has_passed_window(
      cursor_seconds: int,
      schedule_window: ItineraryScheduleWindow ) -> bool:
   return cursor_seconds >= schedule_window.end_seconds


def _aligned_window_start_seconds(
      schedule_window: ItineraryScheduleWindow,
      cursor_seconds: int ) -> int:
   if cursor_seconds < schedule_window.start_seconds:
      return schedule_window.start_seconds

   return cursor_seconds


def _loop_group_fits_in_window(
      schedule_window: ItineraryScheduleWindow,
      *,
      start_seconds: int,
      total_duration_seconds: int ) -> bool:
   return (
      schedule_window.end_seconds - start_seconds
      >= total_duration_seconds )


def _window_index_after_schedule(
      window_match: LoopGroupWindowMatch,
      *,
      end_seconds: int ) -> int:
   if end_seconds >= window_match.schedule_window.end_seconds:
      return window_match.window_index + 1

   return window_match.window_index


def _fetch_viewing_durations(
      conn: Connection,
      animals: list[ ItineraryAnimalRecord ] ) -> list[ int ] | None:
   durations: list[ int ] = []

   for animal_row in animals:
      duration_seconds = fetch_enclosure_viewing_default_duration_seconds(
         conn,
         animal_row.species,
         animal_row.exhibit,
         animal_row.enclosure_name )

      if duration_seconds is None:
         return None

      durations.append( duration_seconds )

   return durations


def _assign_contiguous_slots(
      animals: list[ ItineraryAnimalRecord ],
      durations: list[ int ],
      *,
      start_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ]:
   slots: list[ LoopScheduleSlot ] = []
   slot_cursor_seconds = start_seconds

   for animal_row, duration_seconds in zip( animals, durations ):
      start_time = DateValues.schedule_time_key_from_seconds(
         slot_cursor_seconds )
      end_seconds = slot_cursor_seconds + duration_seconds
      end_time = DateValues.schedule_time_key_from_seconds( end_seconds )

      if start_time is None or end_time is None:
         return [], start_seconds

      slots.append( ( animal_row, start_time, end_time ) )
      slot_cursor_seconds = end_seconds

   return slots, slot_cursor_seconds


def _save_loop_slots(
      conn: Connection,
      blockers: list[ TimeBlock ],
      animal_slots: list[ LoopScheduleSlot ] ) -> bool:
   if not _persist_loop_group_slots( conn, tuple( animal_slots ) ):
      return False

   _append_slots_to_blockers( blockers, tuple( animal_slots ) )

   return True


def _append_slots_to_blockers(
      blockers: list[ TimeBlock ],
      slots: tuple[ LoopScheduleSlot, ... ] ) -> None:
   for _, start_time, end_time in slots:
      scheduled_block = time_block_from_schedule_times(
         start_time,
         end_time )

      if scheduled_block is not None:
         blockers.append( scheduled_block )


def _persist_loop_group_slots(
      conn: Connection,
      scheduled_slots: tuple[ LoopScheduleSlot, ... ] ) -> bool:
   cur = conn.cursor()

   try:
      for animal_row, start_time, end_time in scheduled_slots:
         if not update_itinerary_animal_schedule(
               cur,
               species=animal_row.species,
               exhibit=animal_row.exhibit,
               enclosure_name=animal_row.enclosure_name,
               start_time=start_time,
               end_time=end_time ):
            conn.rollback()
            return False

      conn.commit()
      return True

   finally:
      cur.close()
