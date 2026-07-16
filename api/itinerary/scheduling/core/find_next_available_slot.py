from __future__ import annotations

from ....shared.calendar_dates import DateValues
from ....shared.constants import SCHEDULE_SLOT_STEP_SECONDS
from .time_block import time_blocks_overlap
from .time_block import TimeBlock
from ....types import ScheduleTimeKey


def find_next_available_slot(
      blockers: list[ TimeBlock ],
      anchor_seconds: int,
      duration_seconds: int,
      day_end_seconds: int ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   if anchor_seconds >= day_end_seconds:
      return None

   slot_start = anchor_seconds

   while slot_start + duration_seconds <= day_end_seconds:
      candidate = TimeBlock(
         start_seconds=slot_start,
         end_seconds=slot_start + duration_seconds )

      if not any(
            time_blocks_overlap( candidate, blocker )
            for blocker in blockers ):
         return (
            DateValues.schedule_time_key_from_seconds( slot_start ),
            DateValues.schedule_time_key_from_seconds(
               slot_start + duration_seconds ),
         )

      slot_start += SCHEDULE_SLOT_STEP_SECONDS

   return None


def find_previous_available_slot(
      blockers: list[ TimeBlock ],
      end_before_seconds: int,
      duration_seconds: int,
      day_start_seconds: int ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   if end_before_seconds <= day_start_seconds:
      return None

   slot_end = end_before_seconds

   while slot_end - duration_seconds >= day_start_seconds:
      slot_start = slot_end - duration_seconds
      candidate = TimeBlock(
         start_seconds=slot_start,
         end_seconds=slot_end )

      if not any(
            time_blocks_overlap( candidate, blocker )
            for blocker in blockers ):
         return (
            DateValues.schedule_time_key_from_seconds( slot_start ),
            DateValues.schedule_time_key_from_seconds( slot_end ),
         )

      slot_end -= SCHEDULE_SLOT_STEP_SECONDS

   return None


def find_available_slot_before_or_after_bounds(
      blockers: list[ TimeBlock ],
      duration_seconds: int,
      *,
      day_start_seconds: int,
      day_end_seconds: int,
      before_end_seconds: int,
      after_start_seconds: int,
   ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   """Try a duration-length slot before the bound, then after it."""
   before_slot = find_previous_available_slot(
      blockers,
      before_end_seconds,
      duration_seconds,
      day_start_seconds )

   if before_slot is not None:
      return before_slot

   return find_next_available_slot(
      blockers,
      after_start_seconds,
      duration_seconds,
      day_end_seconds )
