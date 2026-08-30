from __future__ import annotations

from datetime import date

from api.shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver


VISIT_DAY = 15
VISIT_MONTH = 6
VISIT_YEAR = 2026
WEEKDAY_VISIT_DATE = date( VISIT_YEAR, VISIT_MONTH, VISIT_DAY )
WEEKEND_VISIT_DAY = 20
WEEKEND_VISIT_DATE = date( VISIT_YEAR, VISIT_MONTH, WEEKEND_VISIT_DAY )


def Test_Resolve_TestWeekdayVisit_ExpectWeekdayContext() -> None:
   context = OpeningScheduleVisitContextResolver.resolve(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == WEEKDAY_VISIT_DATE
   assert context.normalized_month == VISIT_MONTH
   assert context.normalized_day == VISIT_DAY
   assert context.weekday == WEEKDAY_VISIT_DATE.weekday()
   assert context.is_weekend_or_holiday is False


def Test_Resolve_TestWeekendVisit_ExpectWeekendContext() -> None:
   context = OpeningScheduleVisitContextResolver.resolve(
      day=WEEKEND_VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == WEEKEND_VISIT_DATE
   assert context.is_weekend_or_holiday is True
