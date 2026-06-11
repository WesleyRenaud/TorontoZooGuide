from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .calendar_dates import CalendarDates
from ..types import MonthInput, VisitDay, VisitYear


@dataclass( frozen=True )
class OpeningScheduleVisitContext:
   normalized_month: int
   normalized_day: int
   target_date: date
   weekday: int
   is_weekend_or_holiday: bool


def resolve_opening_schedule_visit_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> OpeningScheduleVisitContext:
   target_date = CalendarDates.visit_target_date(
      month=month,
      day=day,
      year=year )
   weekday = target_date.weekday()
   is_weekend_or_holiday = (
      weekday >= 5
      or CalendarDates.is_holiday( d=target_date ) )

   return OpeningScheduleVisitContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=weekday,
      is_weekend_or_holiday=is_weekend_or_holiday )
