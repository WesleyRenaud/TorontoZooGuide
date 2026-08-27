from __future__ import annotations

from dataclasses import dataclass

from .loop_schedule_stop import LoopScheduleStop


@dataclass( frozen=True )
class LoopPinStopSegment:
   stops: list[ LoopScheduleStop ]
   end_before_seconds: int
   anchor_at_end: bool
