from __future__ import annotations

from api.attractions.scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from api.attractions.scheduling.attraction_hours_schedule_time_bounds_builder import AttractionHoursScheduleTimeBoundsBuilder
from api.attractions.scheduling.attraction_hours_time_bounds import AttractionHoursTimeBounds
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


WEEKDAY_OPERATING_DATE = '2026-06-15'
WEEKEND_OPERATING_DATE = '2026-06-20'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'


def _zoo_hours_record(
      *,
      operating_date: str,
      open_time: str,
      close_time: str ) -> ZooHoursRecord:
   return ZooHoursRecord(
      operating_date=operating_date,
      early_admission_time='9:00 AM',
      open_time=open_time,
      last_admission_time='6:00 PM',
      close_time=close_time )


def Test_ResolveDateRange_TestExplicitDates_ExpectNormalizedRange() -> None:
   start_date, end_date = AttractionHoursScheduleTimeBoundsBuilder.resolve_date_range(
      START_DATE,
      END_DATE )

   assert start_date == START_DATE
   assert end_date == END_DATE


def Test_BuildTimeBounds_TestMultipleRecords_ExpectLatestOpenAndEarliestClose() -> None:
   records = [
      _zoo_hours_record(
         operating_date=WEEKDAY_OPERATING_DATE,
         open_time='9:30 AM',
         close_time='7:00 PM' ),
      _zoo_hours_record(
         operating_date='2026-06-16',
         open_time='10:00 AM',
         close_time='5:00 PM' ),
   ]

   bounds = AttractionHoursScheduleTimeBoundsBuilder._build_time_bounds( records )

   assert bounds is not None
   assert bounds.open_time == '10:00 AM'
   assert bounds.close_time == '5:00 PM'


def Test_RecordsForDayKind_TestWeekdayAndWeekendRecords_ExpectFilteredByDayKind() -> None:
   weekday_record = _zoo_hours_record(
      operating_date=WEEKDAY_OPERATING_DATE,
      open_time='9:30 AM',
      close_time='7:00 PM' )
   weekend_record = _zoo_hours_record(
      operating_date=WEEKEND_OPERATING_DATE,
      open_time='10:00 AM',
      close_time='6:00 PM' )

   weekday_records = AttractionHoursScheduleTimeBoundsBuilder._records_for_day_kind(
      [ weekday_record, weekend_record ],
      weekend_or_holiday=False )
   weekend_records = AttractionHoursScheduleTimeBoundsBuilder._records_for_day_kind(
      [ weekday_record, weekend_record ],
      weekend_or_holiday=True )

   assert weekday_records == [ weekday_record ]
   assert weekend_records == [ weekend_record ]


def Test_TimesAreWithinBounds_TestValidTimes_ExpectTrue() -> None:
   bounds = AttractionHoursScheduleTimeBounds(
      weekday=AttractionHoursTimeBounds(
         open_time='9:30 AM',
         close_time='7:00 PM',
         operating_date=WEEKDAY_OPERATING_DATE ),
      weekend_holiday=AttractionHoursTimeBounds(
         open_time='10:00 AM',
         close_time='6:00 PM',
         operating_date=WEEKEND_OPERATING_DATE ),
   )

   assert AttractionHoursScheduleTimeBoundsBuilder.times_are_within_bounds(
      bounds,
      weekday_start_time='10:00 AM',
      weekday_end_time='4:00 PM',
      weekend_holiday_start_time='11:00 AM',
      weekend_holiday_end_time='5:00 PM' )


def Test_TimesAreWithinBounds_TestOutOfRangeWeekdayEnd_ExpectFalse() -> None:
   bounds = AttractionHoursScheduleTimeBounds(
      weekday=AttractionHoursTimeBounds(
         open_time='9:30 AM',
         close_time='7:00 PM',
         operating_date=WEEKDAY_OPERATING_DATE ),
      weekend_holiday=AttractionHoursTimeBounds(
         open_time='10:00 AM',
         close_time='6:00 PM',
         operating_date=WEEKEND_OPERATING_DATE ),
   )

   assert not AttractionHoursScheduleTimeBoundsBuilder.times_are_within_bounds(
      bounds,
      weekday_start_time='10:00 AM',
      weekday_end_time='8:00 PM',
      weekend_holiday_start_time='11:00 AM',
      weekend_holiday_end_time='5:00 PM' )
