from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from api.shared.enums.schedule_status import ScheduleStatus
from api.shared.opening_schedule_status_resolver import OpeningScheduleStatusResolver


@dataclass
class SampleOpeningScheduleRecord():
   schedule_start_date: str
   schedule_end_date: str | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   holidays_only: bool
   schedule_message: str | None


@dataclass
class SampleScheduleOverrideRecord():
   override_start_date: str
   override_end_date: str | None
   is_closed: bool
   override_message: str | None


MONDAY_VISIT_DATE = date( 2026, 6, 15 )
CANADA_DAY = date( 2026, 7, 1 )
CLOSED_MESSAGE = 'Closed for maintenance.'


def _weekday_schedule(
      *,
      monday: bool = False,
      holidays_only: bool = False,
      schedule_message: str | None = CLOSED_MESSAGE ) -> SampleOpeningScheduleRecord:
   return SampleOpeningScheduleRecord(
      schedule_start_date='2026-01-01',
      schedule_end_date=None,
      monday=monday,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=holidays_only,
      schedule_message=schedule_message )


def Test_GroupRecordsByName_TestDuplicateNames_ExpectGroupedLists() -> None:
   records = [
      SampleOpeningScheduleRecord(
         schedule_start_date='2026-01-01',
         schedule_end_date=None,
         monday=True,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         schedule_message=None ),
      SampleOpeningScheduleRecord(
         schedule_start_date='2026-02-01',
         schedule_end_date=None,
         monday=False,
         tuesday=True,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         schedule_message=None ),
   ]

   grouped = OpeningScheduleStatusResolver.group_records_by_name(
      records,
      lambda record: 'Africa Restaurant' )

   assert len( grouped[ 'Africa Restaurant' ] ) == 2


def Test_GetActiveOpeningScheduleStatus_TestNoSchedules_ExpectUnknown() -> None:
   status, message = OpeningScheduleStatusResolver.get_active_opening_schedule_status(
      schedule_records=[],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday() )

   assert status == ScheduleStatus.UNKNOWN
   assert message is None


def Test_GetActiveOpeningScheduleStatus_TestOutOfRangeDate_ExpectUnknown() -> None:
   out_of_range_schedule = SampleOpeningScheduleRecord(
      schedule_start_date='2026-07-01',
      schedule_end_date='2026-07-31',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      schedule_message=None )

   status, message = OpeningScheduleStatusResolver.get_active_opening_schedule_status(
      schedule_records=[ out_of_range_schedule ],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday() )

   assert status == ScheduleStatus.UNKNOWN
   assert message is None


def Test_GetActiveOpeningScheduleStatus_TestOpenMonday_ExpectOpen() -> None:
   status, message = OpeningScheduleStatusResolver.get_active_opening_schedule_status(
      schedule_records=[ _weekday_schedule( monday=True ) ],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday() )

   assert status == ScheduleStatus.OPEN
   assert message is None


def Test_GetActiveOpeningScheduleStatus_TestHolidayOnlyScheduleOnHoliday_ExpectOpen() -> None:
   status, message = OpeningScheduleStatusResolver.get_active_opening_schedule_status(
      schedule_records=[ _weekday_schedule( holidays_only=True ) ],
      target_date=CANADA_DAY,
      weekday=CANADA_DAY.weekday() )

   assert status == ScheduleStatus.OPEN
   assert message is None


def Test_GetActiveOpeningScheduleStatus_TestClosedWeekday_ExpectClosedMessage() -> None:
   status, message = OpeningScheduleStatusResolver.get_active_opening_schedule_status(
      schedule_records=[ _weekday_schedule() ],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday() )

   assert status == ScheduleStatus.CLOSED
   assert message == CLOSED_MESSAGE


def Test_GetActiveScheduleOverrideStatus_TestClosedOverride_ExpectClosed() -> None:
   override = SampleScheduleOverrideRecord(
      override_start_date='2026-06-01',
      override_end_date=None,
      is_closed=True,
      override_message='Temporarily closed.' )

   status, message = OpeningScheduleStatusResolver.get_active_schedule_override_status(
      override_records=[ override ],
      target_date=MONDAY_VISIT_DATE )

   assert status == ScheduleStatus.CLOSED
   assert message == 'Temporarily closed.'


def Test_CalculateSeasonalLikelihood_TestMultiplier_ExpectRoundedPercent() -> None:
   assert OpeningScheduleStatusResolver.calculate_seasonal_likelihood( 0.45 ) == 45
   assert OpeningScheduleStatusResolver.calculate_seasonal_likelihood( None ) == 100


def Test_ResolveAmenityLikelihoodAndMessage_TestClosedOverride_ExpectZeroLikelihood() -> None:
   override = SampleScheduleOverrideRecord(
      override_start_date='2026-06-01',
      override_end_date=None,
      is_closed=True,
      override_message='Closed today.' )

   likelihood, message = OpeningScheduleStatusResolver.resolve_amenity_likelihood_and_message(
      name='Africa Restaurant',
      schedule_records=[ _weekday_schedule( monday=True ) ],
      override_records=[ override ],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday(),
      seasonal_multiplier=1.0 )

   assert likelihood == 0
   assert message == 'Closed today.'


def Test_ResolveAmenityLikelihoodAndMessage_TestUnknownScheduleWithZeroSeasonal_ExpectLikelyClosedMessage() -> None:
   likelihood, message = OpeningScheduleStatusResolver.resolve_amenity_likelihood_and_message(
      name='Africa Restaurant',
      schedule_records=[],
      override_records=[],
      target_date=MONDAY_VISIT_DATE,
      weekday=MONDAY_VISIT_DATE.weekday(),
      seasonal_multiplier=0.0 )

   assert likelihood == 0
   assert message is not None
   assert 'Africa Restaurant' in message
