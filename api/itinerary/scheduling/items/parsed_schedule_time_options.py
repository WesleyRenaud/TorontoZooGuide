from __future__ import annotations

from dataclasses import dataclass

from ....types import ScheduleTimeKey


@dataclass( frozen=True )
class ParsedScheduleTimeOptions:
   start_time: ScheduleTimeKey
   duration_minutes: int | None

   def to_dict( self ) -> dict[ str, ScheduleTimeKey | int | None ]:
      return {
         'start_time': self.start_time,
         'duration_minutes': self.duration_minutes,
      }
