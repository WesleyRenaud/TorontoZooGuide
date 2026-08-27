from __future__ import annotations

from typing import Union

from .loop_pin_gap_step import LoopPinGapStep
from .loop_pin_stop_segment import LoopPinStopSegment


LoopPinScheduleStep = Union[
   LoopPinStopSegment,
   LoopPinGapStep,
]
