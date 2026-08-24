from __future__ import annotations

from dataclasses import dataclass

from ...shared.operating_hours import OperatingHours
from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ZooHoursRecord:
   operating_date: DateKey
   early_admission_time: ScheduleTimeKey
   open_time: ScheduleTimeKey
   last_admission_time: ScheduleTimeKey
   close_time: ScheduleTimeKey

   def operating_hours( self ) -> OperatingHours | None:
      return OperatingHours.from_schedule_times(
         self.open_time,
         self.close_time )
