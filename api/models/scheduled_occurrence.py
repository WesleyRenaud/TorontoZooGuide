from __future__ import annotations

from ..types import Types


class ScheduledOccurrence:
   def __init__( self, date: Types.DateKey, time: Types.ScheduleTimeKey ) -> None:
      self.date = date
      self.time = time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'date': self.date,
         'time': self.time,
      }
