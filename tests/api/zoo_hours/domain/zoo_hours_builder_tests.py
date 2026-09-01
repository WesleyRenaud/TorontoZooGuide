from __future__ import annotations

from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from api.zoo_hours.domain.zoo_hours_builder import ZooHoursBuilder


JUNE_20_RECORD = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00' )

JUNE_22_RECORD = ZooHoursRecord(
   operating_date='2026-06-22',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='17:00',
   close_time='18:00' )

DECEMBER_25_RECORD = ZooHoursRecord(
   operating_date='2026-12-25',
   early_admission_time=None,
   open_time='11:00',
   last_admission_time='15:00',
   close_time='16:00' )


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


def Test_Build_TestSeededOperatingDates_ExpectToDict() -> None:
   assert ZooHoursBuilder.build( JUNE_20_RECORD ).to_dict() == {
      'date': '2026-06-20',
      'earlyAdmissionTime': '09:00',
      'openTime': '09:30',
      'lastAdmissionTime': '18:00',
      'closeTime': '19:00',
   }
   assert ZooHoursBuilder.build( JUNE_22_RECORD ).to_dict() == {
      'date': '2026-06-22',
      'earlyAdmissionTime': None,
      'openTime': '09:30',
      'lastAdmissionTime': '17:00',
      'closeTime': '18:00',
   }
   assert ZooHoursBuilder.build( DECEMBER_25_RECORD ).to_dict() == {
      'date': '2026-12-25',
      'earlyAdmissionTime': None,
      'openTime': '11:00',
      'lastAdmissionTime': '15:00',
      'closeTime': '16:00',
   }
