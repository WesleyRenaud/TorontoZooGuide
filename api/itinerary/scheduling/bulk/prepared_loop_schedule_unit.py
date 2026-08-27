from __future__ import annotations

from dataclasses import dataclass

from .loop_schedule_unit import LoopScheduleUnit


@dataclass( frozen=True )
class PreparedLoopScheduleUnit:
   unit: LoopScheduleUnit
   occupied_seconds: int
