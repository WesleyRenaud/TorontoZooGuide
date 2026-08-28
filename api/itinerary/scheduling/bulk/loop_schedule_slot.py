from __future__ import annotations

from typing import NamedTuple

from .loop_schedule_stop import LoopScheduleStop
from ....types import Types


class LoopScheduleSlot( NamedTuple ):
   stop: LoopScheduleStop.Stop
   start_time: Types.ScheduleTimeKey
   end_time: Types.ScheduleTimeKey
