from __future__ import annotations

from api.itinerary.scheduling.core.scheduling_anchor_resolver import SchedulingAnchorResolver
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_AnchorSeconds_TestArrivalTime_ExpectArrivalSeconds() -> None:
   assert SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, '09:00' ) == 9 * 3600


def Test_AnchorSeconds_TestNoArrival_ExpectOpenTime() -> None:
   assert SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, None ) == 9 * 3600 + 30 * 60


def Test_AnchorSeconds_TestEarlyAdmissionAllowed_ExpectEarlyAdmissionTime() -> None:
   assert SchedulingAnchorResolver.anchor_seconds(
      ZOO_HOURS,
      None,
      allow_early_admission=True ) == 9 * 3600
