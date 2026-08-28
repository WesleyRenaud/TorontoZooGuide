from __future__ import annotations

from typing import TypeAlias

from .loop_pin_gap_step import LoopPinGapStep
from .loop_pin_stop_segment import LoopPinStopSegment


class LoopPinScheduleStep():
   Step: TypeAlias = LoopPinStopSegment | LoopPinGapStep
