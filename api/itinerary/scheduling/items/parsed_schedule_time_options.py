from __future__ import annotations

from dataclasses import dataclass

from ....types import Types


@dataclass( frozen=True )
class ParsedScheduleTimeOptions:
   start_time: Types.ScheduleTimeKey
   duration_minutes: int | None

   def to_dict( self ) -> dict[ str, Types.ScheduleTimeKey | int | None ]:
      return {
         'start_time': self.start_time,
         'duration_minutes': self.duration_minutes,
      }
