from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from .calendar_dates import CalendarDates


@dataclass( frozen=True )
class PeakMonths():
   weekday_start: int | None = None
   weekday_end: int | None = None
   weekend_start: int | None = None
   weekend_end: int | None = None


   @classmethod
   def from_row( cls, row: Any ) -> PeakMonths:
      return cls(
         weekday_start=row[ 'WEEKDAY_START_MONTH' ],
         weekday_end=row[ 'WEEKDAY_END_MONTH' ],
         weekend_start=row[ 'WEEKEND_START_MONTH' ],
         weekend_end=row[ 'WEEKEND_END_MONTH' ],
      )


   def end_for( self, weekend_only: bool, today: date ) -> date | None:
      start_month = self.weekday_start
      end_month = self.weekday_end

      if weekend_only:
         start_month = self.weekend_start
         end_month = self.weekend_end

      if start_month == None or end_month == None:
         return None

      return CalendarDates.month_end(
         self.ending_year( start_month, end_month, today ),
         end_month,
      )


   def ending_year( self, start_month: int, end_month: int, today: date ) -> int:
      window_wraps_past_december = start_month > end_month
      already_in_start_month = today.month >= start_month

      if window_wraps_past_december and already_in_start_month:
         return today.year + 1

      return today.year


   def day_before_everyday( self, today: date ) -> date | None:
      if self.weekday_start == None:
         return None

      return CalendarDates.one_day_earlier(
         CalendarDates.upcoming_month_start( self.weekday_start, today )
      )


   def extended_end( self, season_end: date | None, today: date ) -> date | None:
      if season_end == None:
         return None

      horizon = CalendarDates.two_weeks_later( today )

      if season_end < horizon:
         return horizon

      return season_end


   def weekend_schedule_end( self, today: date ) -> date | None:
      season_end = self.extended_end( self.end_for( True, today ), today )
      boundary = self.day_before_everyday( today )

      if boundary == None:
         return season_end

      if season_end == None or boundary < season_end:
         return boundary

      return season_end


   def schedule_end( self, weekend_only: bool, today: date ) -> date | None:
      if weekend_only:
         return self.weekend_schedule_end( today )

      return self.extended_end( self.end_for( False, today ), today )
