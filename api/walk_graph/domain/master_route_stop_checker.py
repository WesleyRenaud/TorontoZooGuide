from __future__ import annotations

from .master_route_stop import MasterRouteStop
from ...shared.enums import ScheduleItemKind


class MasterRouteStopChecker():
   @classmethod
   def is_animal( cls, stop: MasterRouteStop.Stop ) -> bool:
      return stop.kind == ScheduleItemKind.ANIMAL


   @classmethod
   def is_attraction( cls, stop: MasterRouteStop.Stop ) -> bool:
      return stop.kind == ScheduleItemKind.ATTRACTION
