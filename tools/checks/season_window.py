from __future__ import annotations

from datetime import date
from datetime import timedelta

from api.shared.calendar_dates import CalendarDates


class SeasonWindow():
   @classmethod
   def needs_week_extension(
         cls,
         closed_today: bool,
         end: date | None,
         today: date ) -> bool:
      if not closed_today:
         return True

      if end == None:
         return False

      return end < CalendarDates.one_week_later( today )


   @classmethod
   def week_extension_end( cls, end: date | None, today: date ) -> date:
      if end != None and end >= today:
         return CalendarDates.one_week_later( end + timedelta( days=1 ) )

      return CalendarDates.one_week_later( today )
