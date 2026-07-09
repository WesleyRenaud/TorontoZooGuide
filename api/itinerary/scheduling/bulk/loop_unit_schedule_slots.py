from __future__ import annotations

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import ScheduleTimeKey


LoopScheduleSlot = tuple[
   ItineraryAnimalRecord,
   ScheduleTimeKey,
   ScheduleTimeKey,
]


def fetch_viewing_durations(
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


def assign_contiguous_slots(
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


def assign_contiguous_slots_ending_by(
      animals: list[ ItineraryAnimalRecord ],
      durations: list[ int ],
      *,
      end_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ] | None:
   total_duration_seconds = sum( durations )
   start_seconds = end_seconds - total_duration_seconds

   if start_seconds < 0:
      return None

   animal_slots, segment_end_cursor_seconds = assign_contiguous_slots(
      animals,
      durations,
      start_seconds=start_seconds )

   if segment_end_cursor_seconds > end_seconds:
      return None

   return animal_slots, segment_end_cursor_seconds


def save_loop_slots(
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
