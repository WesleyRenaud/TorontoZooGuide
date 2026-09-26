from __future__ import annotations

from api.shared.calendar_dates import CalendarDates
from api.shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver


VISIT_DAY = 15
VISIT_MONTH = 6
VISIT_YEAR = 2026
WEEKEND_VISIT_DAY = 20


def Test_Resolve_TestWeekdayVisit_ExpectWeekdayContext() -> None:
   context = OpeningScheduleVisitContextResolver.resolve(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == CalendarDates.visit_target_date(
      VISIT_MONTH,
      VISIT_DAY,
      VISIT_YEAR )
   assert context.normalized_month == VISIT_MONTH
   assert context.normalized_day == VISIT_DAY
   assert context.weekday == context.target_date.weekday()
   assert context.is_weekend_or_holiday is CalendarDates.is_weekend_or_holiday(
      context.target_date )


def Test_Resolve_TestWeekendVisit_ExpectWeekendContext() -> None:
   context = OpeningScheduleVisitContextResolver.resolve(
      day=WEEKEND_VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == CalendarDates.visit_target_date(
      VISIT_MONTH,
      WEEKEND_VISIT_DAY,
      VISIT_YEAR )
   assert context.is_weekend_or_holiday is CalendarDates.is_weekend_or_holiday(
      context.target_date )
