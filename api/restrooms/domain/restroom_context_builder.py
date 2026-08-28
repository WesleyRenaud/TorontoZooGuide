from __future__ import annotations

from .restroom_context import RestroomContext
from ...shared.calendar_dates import CalendarDates
from ...types import Types


class RestroomContextBuilder():
   @classmethod
   def resolve(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear ) -> RestroomContext:
      return RestroomContext(
         target_date=CalendarDates.visit_target_date(
            month=month,
            day=day,
            year=year ) )
