from __future__ import annotations

from ..types import Types


class ZooHours:
   def __init__(
         self,
         date: Types.DateKey,
         early_admission_time: Types.ScheduleTimeKey,
         open_time: Types.ScheduleTimeKey,
         last_admission_time: Types.ScheduleTimeKey,
         close_time: Types.ScheduleTimeKey ) -> None:

      self.date = date
      self.early_admission_time = early_admission_time
      self.open_time = open_time
      self.last_admission_time = last_admission_time
      self.close_time = close_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'date': self.date,
         'earlyAdmissionTime': self.early_admission_time,
         'openTime': self.open_time,
         'lastAdmissionTime': self.last_admission_time,
         'closeTime': self.close_time,
      }
