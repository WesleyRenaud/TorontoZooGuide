from __future__ import annotations

from .loop_schedule_stop import LoopScheduleStop
from ....types import ScheduleTimeKey


LoopScheduleSlot = tuple[
   LoopScheduleStop,
   ScheduleTimeKey,
   ScheduleTimeKey,
]
