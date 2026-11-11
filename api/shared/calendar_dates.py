from __future__ import annotations

import calendar
from datetime import date, timedelta
from typing import Any

from .date_values import DateValues
from ..types import Types


class CalendarDates:
   MONTH_ABBREVIATIONS = (
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
   )
   DAYS_IN_MONTH = ( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 )


   @staticmethod
   def convert_weekday( weekday: int, sunday_first: bool ) -> int:
      offset = 1 if sunday_first else -1
      return ( weekday + offset ) % 7


   @staticmethod
   def format_weekdays( weekdays: set[ int ] ) -> str:
      ordered = sorted(
         weekdays,
         key=lambda weekday: CalendarDates.convert_weekday( weekday, sunday_first=True ),
      )

      return ', '.join(
         calendar.day_abbr[ weekday ]
         for weekday in ordered
      )


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
   def month_index( name: str ) -> int | None:
      folded = name.casefold()

      for index, month_name in enumerate( calendar.month_name ):
         if month_name and month_name.casefold() == folded:
            return index

      return None


   @staticmethod
   def resolve_month_day( month: int, day: int, today: date ) -> date:
      this_year = date( today.year, month, day )

      if this_year < today:
         return this_year.replace( year=today.year + 1 )

      return this_year


   @staticmethod
   def next_month_end( month: int, today: date ) -> date:
      end = CalendarDates.month_end( today.year, month )

      if end < today:
         end = CalendarDates.month_end( today.year + 1, month )

      return end


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

         index = CalendarDates.month_index( month )

         if index is not None:
            return CalendarDates.MONTH_ABBREVIATIONS[ index - 1 ]

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
   def one_day_earlier( day: date ) -> date:
      return day - timedelta( days=1 )


   @staticmethod
   def one_day_later( day: date ) -> date:
      return day + timedelta( days=1 )


   @staticmethod
   def one_week_later( day: date ) -> date:
      return day + timedelta( days=7 )


   @staticmethod
   def upcoming_month_start( month: int, today: date ) -> date:
      opening = date( today.year, month, 1 )

      if opening <= today:
         return date( today.year + 1, month, 1 )

      return opening


   @staticmethod
   def next_month_start( year: int, month: int ) -> date:
      if month == 12:
         return date( year + 1, 1, 1 )

      return date( year, month + 1, 1 )


   @staticmethod
   def month_end( year: int, month: int ) -> date:
      _first_weekday, number_of_days = calendar.monthrange( year, month )
      return date( year, month, number_of_days )


   @staticmethod
   def two_weeks_later( day: date ) -> date:
      return day + timedelta( days=14 )


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

      return CalendarDates.one_week_later( d )
