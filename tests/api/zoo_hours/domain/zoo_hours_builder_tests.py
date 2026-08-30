from __future__ import annotations

from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from api.zoo_hours.domain.zoo_hours_builder import ZooHoursBuilder


def Test_Build_TestZooHoursRecord_ExpectMapsOperatingHours() -> None:
   record = ZooHoursRecord(
      operating_date='2026-06-20',
      early_admission_time='09:00',
      open_time='09:30',
      last_admission_time='18:00',
      close_time='19:00' )

   hours = ZooHoursBuilder.build( record )

   assert hours.date == '2026-06-20'
   assert hours.early_admission_time == '09:00'
   assert hours.open_time == '09:30'
   assert hours.last_admission_time == '18:00'
   assert hours.close_time == '19:00'
