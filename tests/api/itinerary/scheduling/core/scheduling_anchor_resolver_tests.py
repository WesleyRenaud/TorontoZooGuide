from __future__ import annotations

from api.itinerary.scheduling.core.scheduling_anchor_resolver import SchedulingAnchorResolver
from api.shared.calendar_dates import DateValues
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_CoveringFixedZooStarts_TestInvalidFixedStart_ExpectSkipsInvalid() -> None:
   arrival_time = '9:30 AM'
   earlier_fixed_start = '9:00 AM'

   seconds = SchedulingAnchorResolver.covering_fixed_zoo_starts(
      ZOO_HOURS,
      arrival_time,
      [ '', earlier_fixed_start ] )

   assert seconds == DateValues.time_value_in_seconds( earlier_fixed_start )


def Test_DayEndSeconds_TestInvalidCloseTime_ExpectNone() -> None:
   invalid_hours = ZooHoursRecord(
      operating_date=ZOO_HOURS.operating_date,
      early_admission_time=ZOO_HOURS.early_admission_time,
      open_time=ZOO_HOURS.open_time,
      last_admission_time=ZOO_HOURS.last_admission_time,
      close_time='',
   )

   seconds = SchedulingAnchorResolver.day_end_seconds( invalid_hours, '5:00 PM' )

   assert seconds is None


def Test_DayEndSeconds_TestInvalidDeparture_ExpectCloseSeconds() -> None:
   seconds = SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, '' )

   assert seconds == DateValues.time_value_in_seconds( ZOO_HOURS.close_time )


def Test_AnchorSeconds_TestArrivalTime_ExpectArrivalSeconds() -> None:
   arrival_time = '09:00'

   seconds = SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, arrival_time )

   assert seconds == DateValues.time_value_in_seconds( arrival_time )


def Test_AnchorSeconds_TestNoArrival_ExpectOpenTime() -> None:
   seconds = SchedulingAnchorResolver.anchor_seconds( ZOO_HOURS, None )

   assert seconds == DateValues.time_value_in_seconds( ZOO_HOURS.open_time )


def Test_AnchorSeconds_TestEarlyAdmissionAllowed_ExpectEarlyAdmissionTime() -> None:
   seconds = SchedulingAnchorResolver.anchor_seconds(
      ZOO_HOURS,
      None,
      allow_early_admission=True )

   assert seconds == DateValues.time_value_in_seconds( ZOO_HOURS.early_admission_time )


def Test_CoveringFixedZooStarts_TestEarlierFixedStart_ExpectPulledEarlier() -> None:
   arrival_time = '9:30 AM'
   earlier_fixed_start = '9:00 AM'

   seconds = SchedulingAnchorResolver.covering_fixed_zoo_starts(
      ZOO_HOURS,
      arrival_time,
      [ earlier_fixed_start ] )

   assert seconds == DateValues.time_value_in_seconds( earlier_fixed_start )


def Test_DayEndSeconds_TestDepartureBeforeClose_ExpectDepartureSeconds() -> None:
   departure_time = '5:00 PM'

   seconds = SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, departure_time )

   assert seconds == DateValues.time_value_in_seconds( departure_time )


def Test_DayEndSeconds_TestDepartureAfterClose_ExpectCloseSeconds() -> None:
   departure_time = '8:00 PM'

   seconds = SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, departure_time )

   assert seconds == DateValues.time_value_in_seconds( ZOO_HOURS.close_time )


def Test_DayEndSeconds_TestUnsetDeparture_ExpectCloseSeconds() -> None:
   seconds = SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, None )

   assert seconds == DateValues.time_value_in_seconds( ZOO_HOURS.close_time )
