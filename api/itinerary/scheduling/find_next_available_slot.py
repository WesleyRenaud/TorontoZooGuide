from __future__ import annotations

from ...shared.constants import SCHEDULE_SLOT_STEP_MINUTES
from ...shared.date_values import DateValues
from .time_block import time_blocks_overlap
from .time_block import TimeBlock
from ...types import ScheduleTimeKey


def find_next_available_slot(
      blockers: list[ TimeBlock ],
      anchor_minutes: int,
      duration_minutes: int,
      day_end_minutes: int ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   if anchor_minutes >= day_end_minutes:
      return None

   slot_start = anchor_minutes

   while slot_start + duration_minutes <= day_end_minutes:
      candidate = TimeBlock(
         start_minutes=slot_start,
         end_minutes=slot_start + duration_minutes )

      if not any(
            time_blocks_overlap( candidate, blocker )
            for blocker in blockers ):
         return (
            DateValues.schedule_time_key_from_minutes( slot_start ),
            DateValues.schedule_time_key_from_minutes(
               slot_start + duration_minutes ),
         )

      slot_start += SCHEDULE_SLOT_STEP_MINUTES

   return None
