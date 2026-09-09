from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .date_values import DateValues
from ..types import Types


class CalendarDates:
   MONTH_ABBREVIATIONS = (
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
   )
   MONTH_FULL_NAME_TO_INDEX = {
      'january': 1,
      'february': 2,
      'march': 3,
      'april': 4,
      'may': 5,
      'june': 6,
      'july': 7,
      'august': 8,
      'september': 9,
      'october': 10,
      'november': 11,
      'december': 12,
   }
   DAYS_IN_MONTH = ( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 )


   @staticmethod
   def normalize_month( month: Types.MonthInput ) -> Types.VisitMonth | None:
      if not month:
         return None

      if isinstance( month, int ):
         if 1 <= month <= 12:
            return month
         return None

      m = str( month ).strip()

      for index, label in enumerate( CalendarDates.MONTH_ABBREVIATIONS, start=1 ):
         upper = label.upper()

         if m in ( upper, label ) or m.startswith( label ) or m.startswith( upper ):
            return index

      return None


   @staticmethod
   def get_month_abbreviation( month: Types.MonthInput ) -> str:
      if isinstance( month, int ):
         if month < 1 or month > 12:
            raise ValueError( f'Invalid month: { month }' )
         return CalendarDates.MONTH_ABBREVIATIONS[ month - 1 ]

      if isinstance( month, str ):
         month = month.strip()

         if month.isdigit():
            month_num = int( month )
            if month_num < 1 or month_num > 12:
               raise ValueError( f'Invalid month: { month }' )
            return CalendarDates.MONTH_ABBREVIATIONS[ month_num - 1 ]

         lowered = month.lower()

         if lowered in CalendarDates.MONTH_FULL_NAME_TO_INDEX:
            return CalendarDates.MONTH_ABBREVIATIONS[
               CalendarDates.MONTH_FULL_NAME_TO_INDEX[ lowered ] - 1
            ]

         abbrev = month[ :3 ].title()
         if abbrev in CalendarDates.MONTH_ABBREVIATIONS:
            return abbrev

      raise ValueError( f'Invalid month: { month }' )


   @staticmethod
   def resolve_visit_calendar_month( month: Types.MonthInput ) -> Types.VisitMonth:
      label = CalendarDates.get_month_abbreviation( month )
      index = CalendarDates.normalize_month( month=label )

      if index is None:
         raise ValueError( f'Invalid month: { repr( month ) }' )

      return index


   @staticmethod
   def resolve_visit_day_of_month( day: Types.VisitDay | str ) -> Types.VisitDay:
      return int( day )


   @staticmethod
   def resolve_visit_calendar_year( calendar_year: Types.VisitYear | None = None ) -> Types.VisitYear:
      if calendar_year is not None:
         return int( calendar_year )

      return DateValues.parse_date_value( DateValues.today_date_key() ).year


   @staticmethod
   def visit_target_date( month: Types.MonthInput, day: Types.VisitDay | str, year: Types.VisitYear | None ) -> date:
      return date(
         int( CalendarDates.resolve_visit_calendar_year( year ) ),
         int( CalendarDates.resolve_visit_calendar_month( month ) ),
         int( CalendarDates.resolve_visit_day_of_month( day ) ),
      )


   @staticmethod
   def schedule_includes_weekday( weekday_index: int, monday_through_sunday: list[ Any ] ) -> bool:
      if weekday_index < 0 or weekday_index > 6:
         return False

      return bool( monday_through_sunday[ weekday_index ] )


   @staticmethod
   def get_day_of_year( month: str, day: int ) -> int:
      month_index = CalendarDates.normalize_month( month )

      if month_index is None:
         raise KeyError( month )

      doy = sum( CalendarDates.DAYS_IN_MONTH[ :month_index - 1 ] )
      return doy + ( day - 1 )


   @staticmethod
   def get_next_month( month: str ) -> str | None:
      month_index = CalendarDates.normalize_month( month )

      if month_index is None:
         return None

      next_index = 1 if month_index == 12 else month_index + 1
      return CalendarDates.MONTH_ABBREVIATIONS[ next_index - 1 ]


   @staticmethod
   def get_number_of_days_in_month( month: str ) -> int | None:
      month_index = CalendarDates.normalize_month( month )

      if month_index is None:
         return None

      return CalendarDates.DAYS_IN_MONTH[ month_index - 1 ]


   @staticmethod
   def is_peak_season_month( month: Types.MonthInput ) -> bool:
      month = CalendarDates.normalize_month( month )

      if month >= 5 and month <= 10:
         return True

      return False


   @staticmethod
   def is_holiday( d: date ) -> bool:
      year = d.year

      holidays = {
         date( year, 1, 1 ),
         CalendarDates.get_family_day( year ),
         CalendarDates.get_good_friday( year ),
         CalendarDates.get_victoria_day( year ),
         date( year, 7, 1 ),
         CalendarDates.get_civic_holiday( year ),
         CalendarDates.get_labour_day( year ),
         CalendarDates.get_thanksgiving( year ),
         date( year, 12, 25 )
      }

      return d in holidays


   @staticmethod
   def is_weekend_or_holiday( d: date ) -> bool:
      return (
         d.weekday() >= 5
         or CalendarDates.is_holiday( d=d )
      )


   @staticmethod
   def next_weekday_date( d: date ) -> date:
      while CalendarDates.is_weekend_or_holiday( d=d ):
         d += timedelta( days=1 )

      return d


   @staticmethod
   def next_weekend_or_holiday_date( d: date ) -> date:
      while not CalendarDates.is_weekend_or_holiday( d=d ):
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_family_day( year: Types.VisitYear ) -> date:
      d = date( year, 2, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=14 )


   @staticmethod
   def get_good_friday( year: Types.VisitYear ) -> date:
      easter = CalendarDates.get_easter_date( year )
      return easter - timedelta( days=2 )


   @staticmethod
   def get_easter_date( year: Types.VisitYear ) -> date:
      a = year % 19
      b = year // 100
      c = year % 100
      d = b // 4
      e = b % 4
      f = ( b + 8 ) // 25
      g = ( b - f + 1 ) // 3
      h = ( 19 * a + b - d - g + 15 ) % 30
      i = c // 4
      k = c % 4
      weekday_offset = ( 32 + 2 * e + 2 * i - h - k ) % 7
      m = ( a + 11 * h + 22 * weekday_offset ) // 451
      month = ( h + weekday_offset - 7 * m + 114 ) // 31
      day = ( ( h + weekday_offset - 7 * m + 114 ) % 31 ) + 1

      return date( year, month, day )


   @staticmethod
   def get_victoria_day( year: Types.VisitYear ) -> date:
      d = date( year, 5, 24 )

      while d.weekday() != 0:
         d -= timedelta( days=1 )

      return d


   @staticmethod
   def get_civic_holiday( year: Types.VisitYear ) -> date:
      d = date( year, 8, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_labour_day( year: Types.VisitYear ) -> date:
      d = date( year, 9, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_thanksgiving( year: Types.VisitYear ) -> date:
      d = date( year, 10, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=7 )
