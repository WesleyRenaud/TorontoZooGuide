from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.calendar_dates import CalendarDates
from ...shared.peak_months import PeakMonths


@dataclass( frozen=True )
class ExhibitSeason():
   open_start: int | None = None
   open_end: int | None = None
   name: str = ''


   def in_open_season( self, today: date ) -> bool:
      if self.open_start is None or self.open_end is None:
         return False

      return self.open_start <= today.month <= self.open_end


   def closed_until_month( self ) -> int | None:
      if self.open_start is None:
         return None

      return CalendarDates.previous_month( self.open_start )


   def window_end( self, closed: bool, today: date ) -> date | None:
      if self.open_start is None or self.open_end is None:
         return None

      if closed:
         if self.in_open_season( today ):
            return None

         return CalendarDates.next_month_end( self.closed_until_month(), today )

      return PeakMonths( self.open_start, self.open_end ).end_for( False, today )


   def end_for( self, closed: bool, today: date ) -> date:
      window = self.window_end( closed, today )
      horizon = CalendarDates.two_weeks_later( today )

      if window is None or window < horizon:
         return horizon

      return window
