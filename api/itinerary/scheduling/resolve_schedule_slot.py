from __future__ import annotations

from .find_next_available_slot import find_next_available_slot
from ...shared.date_values import DateValues
from .time_block import time_blocks_overlap
from .time_block import TimeBlock
from ...types import ScheduleTimeKey


def resolve_schedule_slot(
      blockers: list[ TimeBlock ],
      anchor_minutes: int,
      duration_minutes: int,
      day_end_minutes: int,
      *,
      start_time: ScheduleTimeKey | None = None,
) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   if start_time is None:
      return find_next_available_slot(
         blockers,
         anchor_minutes,
         duration_minutes,
         day_end_minutes )

   start_minutes = DateValues.time_value_in_minutes( start_time )
   end_minutes = start_minutes + duration_minutes

   if (
         start_minutes < anchor_minutes
         or end_minutes > day_end_minutes ):
      return None

   candidate = TimeBlock(
      start_minutes=start_minutes,
      end_minutes=end_minutes )

   if any(
         time_blocks_overlap( candidate, blocker )
         for blocker in blockers ):
      return None

   return (
      DateValues.schedule_time_key_from_minutes( start_minutes ),
      DateValues.schedule_time_key_from_minutes( end_minutes ),
   )
