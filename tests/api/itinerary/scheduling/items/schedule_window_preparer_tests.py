from __future__ import annotations

from api.itinerary.scheduling.items.schedule_window_preparer import ScheduleWindowPreparer
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-15',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)

EARLY_ADMISSION_ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_ZooHoursWindowSeconds_TestStandardHours_ExpectOpenToClose() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS ) == (
      9 * 3600 + 30 * 60,
      19 * 3600,
   )


def Test_ZooHoursWindowSeconds_TestEarlyAdmission_ExpectEarlierAnchor() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      EARLY_ADMISSION_ZOO_HOURS,
      allow_early_admission=True ) == (
      9 * 3600,
      19 * 3600,
   )


def Test_ZooHoursWindowSeconds_TestFixedZooStartTimes_ExpectEarlierAnchor() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS,
      fixed_zoo_start_times=[ '09:00 AM' ] ) == (
      9 * 3600,
      19 * 3600,
   )
