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


def Test_CoveringFixedZooStarts_TestInvalidFixedStart_ExpectSkipsInvalid() -> None:
   assert SchedulingAnchorResolver.covering_fixed_zoo_starts(
      ZOO_HOURS,
      '9:30 AM',
      [ '', '9:00 AM' ] ) == 9 * 3600


def Test_DayEndSeconds_TestInvalidCloseTime_ExpectNone() -> None:
   invalid_hours = ZooHoursRecord(
      operating_date='2026-06-20',
      early_admission_time='09:00',
      open_time='09:30',
      last_admission_time='18:00',
      close_time='',
   )

   assert SchedulingAnchorResolver.day_end_seconds( invalid_hours, '5:00 PM' ) is None


def Test_DayEndSeconds_TestInvalidDeparture_ExpectCloseSeconds() -> None:
   assert SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, '' ) == 19 * 3600


def Test_AnchorSeconds_TestArrivalTime_ExpectArrivalSeconds() -> None:
   assert SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, '09:00' ) == 9 * 3600


def Test_AnchorSeconds_TestNoArrival_ExpectOpenTime() -> None:
   assert SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, None ) == 9 * 3600 + 30 * 60


def Test_AnchorSeconds_TestEarlyAdmissionAllowed_ExpectEarlyAdmissionTime() -> None:
   assert SchedulingAnchorResolver.anchor_seconds(
      ZOO_HOURS,
      None,
      allow_early_admission=True ) == 9 * 3600


def Test_CoveringFixedZooStarts_TestEarlierFixedStart_ExpectPulledEarlier() -> None:
   assert SchedulingAnchorResolver.covering_fixed_zoo_starts(
      ZOO_HOURS,
      '9:30 AM',
      [ '9:00 AM' ] ) == 9 * 3600


def Test_DayEndSeconds_TestDepartureBeforeClose_ExpectDepartureSeconds() -> None:
   assert SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, '5:00 PM' ) == 17 * 3600


def Test_DayEndSeconds_TestDepartureAfterClose_ExpectCloseSeconds() -> None:
   assert SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, '8:00 PM' ) == 19 * 3600


def Test_DayEndSeconds_TestUnsetDeparture_ExpectCloseSeconds() -> None:
   assert SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, None ) == 19 * 3600
