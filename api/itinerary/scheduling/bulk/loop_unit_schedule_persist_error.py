from __future__ import annotations

from .loop_schedule_stop import LoopScheduleStop


class LoopUnitSchedulePersistError( Exception ):
   def __init__( self, stops: list[ LoopScheduleStop ] ) -> None:
      self.stops = stops
      super().__init__()
