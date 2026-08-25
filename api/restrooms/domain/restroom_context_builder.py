from __future__ import annotations

from .restroom_context import RestroomContext
from ...shared.calendar_dates import CalendarDates
from ...types import MonthInput, VisitDay, VisitYear


class RestroomContextBuilder():
   @classmethod
   def resolve(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> RestroomContext:
      return RestroomContext(
         target_date=CalendarDates.visit_target_date(
            month=month,
            day=day,
            year=year ) )
