from __future__ import annotations

from dataclasses import dataclass

from ...shared.operating_hours import OperatingHours
from ...types import Types


@dataclass( frozen=True )
class ZooHoursRecord:
   operating_date: Types.DateKey
   early_admission_time: Types.ScheduleTimeKey
   open_time: Types.ScheduleTimeKey
   last_admission_time: Types.ScheduleTimeKey
   close_time: Types.ScheduleTimeKey

   def operating_hours( self ) -> OperatingHours | None:
      return OperatingHours.from_schedule_times(
         self.open_time,
         self.close_time )
