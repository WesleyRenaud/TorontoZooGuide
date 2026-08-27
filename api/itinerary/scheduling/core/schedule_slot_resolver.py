from __future__ import annotations

from .available_schedule_slot_finder import AvailableScheduleSlotFinder
from ....shared.calendar_dates import DateValues
from .time_block import TimeBlock
from .time_block_builder import TimeBlockBuilder
from ....types import ScheduleTimeKey


class ScheduleSlotResolver():
   @classmethod
   def resolve(
         cls,
         blockers: list[ TimeBlock ],
         anchor_seconds: int,
         duration_seconds: int,
         day_end_seconds: int,
         *,
         start_time: ScheduleTimeKey | None = None ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
      if start_time is None:
         return AvailableScheduleSlotFinder.find_next(
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
            TimeBlockBuilder.overlap( candidate, blocker )
            for blocker in blockers ):
         return None

      return (
         DateValues.schedule_time_key_from_seconds( start_seconds ),
         DateValues.schedule_time_key_from_seconds( end_seconds ),
      )
