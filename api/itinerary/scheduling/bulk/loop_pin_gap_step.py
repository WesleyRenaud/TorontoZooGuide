from __future__ import annotations

from dataclasses import dataclass

from ...routing.loop_schedule_pin import LoopSchedulePin


@dataclass( frozen=True )
class LoopPinGapStep:
   loop_pin: LoopSchedulePin
