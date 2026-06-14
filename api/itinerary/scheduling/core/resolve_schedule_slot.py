from __future__ import annotations

from .find_next_available_slot import find_next_available_slot
from ....shared.calendar_dates import DateValues
from .time_block import time_blocks_overlap
from .time_block import TimeBlock
from ....types import ScheduleTimeKey


def resolve_schedule_slot(
      blockers: list[ TimeBlock ],
      anchor_seconds: int,
      duration_seconds: int,
      day_end_seconds: int,
      *,
      start_time: ScheduleTimeKey | None = None ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   if start_time is None:
      return find_next_available_slot(
         blockers,
         anchor_seconds,
         duration_seconds,
         day_end_seconds )

   start_seconds = DateValues.time_value_in_seconds( start_time )

   if start_seconds is None:
      return None

   end_seconds = start_seconds + duration_seconds

   if (
         start_seconds < anchor_seconds
         or end_seconds > day_end_seconds ):
      return None

   candidate = TimeBlock(
      start_seconds=start_seconds,
      end_seconds=end_seconds )

   if any(
         time_blocks_overlap( candidate, blocker )
         for blocker in blockers ):
      return None

   return (
      DateValues.schedule_time_key_from_seconds( start_seconds ),
      DateValues.schedule_time_key_from_seconds( end_seconds ),
   )
