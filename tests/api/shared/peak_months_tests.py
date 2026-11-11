from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import CalendarDates
from api.shared.peak_months import PeakMonths


JUNE_THROUGH_OCTOBER = PeakMonths( 6, 10, 6, 10 )
WEEKDAY_AND_WEEKEND = PeakMonths( 6, 8, 6, 10 )


def _month_end( today: date, month: int ) -> date:
   return CalendarDates.month_end( today.year, month )


def Test_EndingYear_TestDecemberInWrappedWindow_ExpectNextYear() -> None:
   today = date( 2026, 12, 1 )
   months = PeakMonths( 11, 3, 11, 3 )

   year = months.ending_year( 11, 3, today )

   assert year == today.year + 1
   assert months.end_for( False, today ) == CalendarDates.month_end( year, 3 )


def Test_ScheduleEnd_TestOctober1InJuneThroughOctober_ExpectMonthEnd() -> None:
   today = date( 2026, 10, 1 )

   end = JUNE_THROUGH_OCTOBER.schedule_end( False, today )

   assert end == _month_end( today, 10 )


def Test_ScheduleEnd_TestOctober25InJuneThroughOctober_ExpectTwoWeeks() -> None:
   today = date( 2026, 10, 25 )

   end = JUNE_THROUGH_OCTOBER.schedule_end( False, today )

   assert end == CalendarDates.two_weeks_later( today )


def Test_ScheduleEnd_TestNovember1InJuneThroughOctober_ExpectTwoWeeks() -> None:
   today = date( 2026, 11, 1 )

   end = JUNE_THROUGH_OCTOBER.schedule_end( False, today )

   assert end == CalendarDates.two_weeks_later( today )


def Test_ScheduleEnd_TestSeptemberEveryday_ExpectTwoWeeks() -> None:
   today = date( 2026, 9, 1 )

   end = WEEKDAY_AND_WEEKEND.schedule_end( False, today )

   assert end == CalendarDates.two_weeks_later( today )


def Test_ScheduleEnd_TestSeptemberWeekends_ExpectOctoberEnd() -> None:
   today = date( 2026, 9, 1 )

   end = WEEKDAY_AND_WEEKEND.schedule_end( True, today )

   assert end == _month_end( today, 10 )


def Test_ScheduleEnd_TestNoMonths_ExpectNoEnd() -> None:
   months = PeakMonths()
   today = date( 2026, 11, 9 )

   assert months.schedule_end( False, today ) == None
   assert months.schedule_end( True, today ) == None


def Test_ScheduleEnd_TestWeekendBeforeAprilEveryday_ExpectMarch31() -> None:
   months = PeakMonths( 4, 10 )
   today = date( 2026, 11, 11 )

   end = months.schedule_end( True, today )

   assert end == date( 2027, 3, 31 )


def Test_ScheduleEnd_TestWeekendInFebruaryBeforeApril_ExpectMarch31() -> None:
   months = PeakMonths( 4, 10 )
   today = date( 2026, 2, 10 )

   end = months.schedule_end( True, today )

   assert end == date( 2026, 3, 31 )


def Test_ScheduleEnd_TestWeekendWithinTwoWeeksOfApril_ExpectMarch31() -> None:
   months = PeakMonths( 4, 10 )
   today = date( 2026, 3, 20 )

   end = months.schedule_end( True, today )

   assert end == date( 2026, 3, 31 )


def Test_ScheduleEnd_TestWeekendEndBeforeEveryday_ExpectWeekendEnd() -> None:
   months = PeakMonths( 5, 10, 3, 12 )
   today = date( 2026, 11, 11 )

   end = months.schedule_end( True, today )

   assert end == _month_end( today, 12 )
