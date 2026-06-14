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
