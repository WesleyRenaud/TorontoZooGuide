from __future__ import annotations

from .calendar_dates import CalendarDates
from .opening_schedule_visit_context import OpeningScheduleVisitContext
from ..types import Types


class OpeningScheduleVisitContextResolver():
   @classmethod
   def resolve(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear ) -> OpeningScheduleVisitContext:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )
      weekday = target_date.weekday()
      is_weekend_or_holiday = CalendarDates.is_weekend_or_holiday( d=target_date )

      return OpeningScheduleVisitContext(
         normalized_month=target_date.month,
         normalized_day=target_date.day,
         target_date=target_date,
         weekday=weekday,
         is_weekend_or_holiday=is_weekend_or_holiday )
