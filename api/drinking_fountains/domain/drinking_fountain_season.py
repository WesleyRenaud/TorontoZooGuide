from __future__ import annotations

from datetime import date

from ...shared.calendar_dates import CalendarDates


class DrinkingFountainSeason():
   OPEN_START_MONTH = 5
   OPEN_END_MONTH = 10


   @classmethod
   def open_season( cls, today: date ) -> bool:
      return cls.OPEN_START_MONTH <= today.month <= cls.OPEN_END_MONTH


   @classmethod
   def closed_until_month( cls ) -> int:
      return CalendarDates.previous_month( cls.OPEN_START_MONTH )


   @classmethod
   def closed_end( cls, today: date ) -> date:
      if cls.open_season( today ):
         return CalendarDates.two_weeks_later( today )

      return CalendarDates.next_month_end( cls.closed_until_month(), today )


   @classmethod
   def open_end( cls, today: date ) -> date:
      if not cls.open_season( today ):
         return CalendarDates.two_weeks_later( today )

      return CalendarDates.month_end( today.year, cls.OPEN_END_MONTH )


   @classmethod
   def end_for( cls, closed: bool, today: date ) -> date:
      if closed:
         return cls.closed_end( today )

      return cls.open_end( today )
