from __future__ import annotations

from dataclasses import dataclass

from .loop_schedule_stop import LoopScheduleStop


@dataclass( frozen=True )
class TimedLoopScheduleStop:
   stop: LoopScheduleStop.Stop
   duration_seconds: int
   travel_before_seconds: int


   def occupied_seconds( self ) -> int:
      return self.travel_before_seconds + self.duration_seconds
