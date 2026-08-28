from __future__ import annotations

from datetime import date, timedelta

from .date_values import DateValues
from ..types import Types


class CalendarDates:
   @staticmethod
   def normalize_month( month: Types.MonthInput ) -> Types.VisitMonth | None:
      if not month:
         return None

      if isinstance( month, int ):
         if 1 <= month <= 12:
            return month
         return None

      m = str( month ).strip()

      if m in ( 'JAN', 'Jan' ) or m.startswith( 'Jan' ) or m.startswith( 'JAN' ):
         return 1
      elif m in ( 'FEB', 'Feb' ) or m.startswith( 'Feb' ) or m.startswith( 'FEB' ):
         return 2
      elif m in ( 'MAR', 'Mar' ) or m.startswith( 'Mar' ) or m.startswith( 'MAR' ):
         return 3
      elif m in ( 'APR', 'Apr' ) or m.startswith( 'Apr' ) or m.startswith( 'APR' ):
         return 4
      elif m in ( 'MAY', 'May' ) or m.startswith( 'May' ) or m.startswith( 'MAY' ):
         return 5
      elif m in ( 'JUN', 'Jun' ) or m.startswith( 'Jun' ) or m.startswith( 'JUN' ):
         return 6
      elif m in ( 'JUL', 'Jul' ) or m.startswith( 'Jul' ) or m.startswith( 'JUL' ):
         return 7
      elif m in ( 'AUG', 'Aug' ) or m.startswith( 'Aug' ) or m.startswith( 'AUG' ):
         return 8
      elif m in ( 'SEP', 'Sep' ) or m.startswith( 'Sep' ) or m.startswith( 'SEP' ):
         return 9
      elif m in ( 'OCT', 'Oct' ) or m.startswith( 'Oct' ) or m.startswith( 'OCT' ):
         return 10
      elif m in ( 'NOV', 'Nov' ) or m.startswith( 'Nov' ) or m.startswith( 'NOV' ):
         return 11
      elif m in ( 'DEC', 'Dec' ) or m.startswith( 'Dec' ) or m.startswith( 'DEC' ):
         return 12

      return None


   @staticmethod
   def get_month_abbreviation( month: Types.MonthInput ) -> str:
      month_map = {
         1: 'Jan',
         2: 'Feb',
         3: 'Mar',
         4: 'Apr',
         5: 'May',
         6: 'Jun',
         7: 'Jul',
         8: 'Aug',
         9: 'Sep',
         10: 'Oct',
         11: 'Nov',
         12: 'Dec',
      }

      full_name_map = {
         'january': 'Jan',
         'february': 'Feb',
         'march': 'Mar',
         'april': 'Apr',
         'may': 'May',
         'june': 'Jun',
         'july': 'Jul',
         'august': 'Aug',
         'september': 'Sep',
         'october': 'Oct',
         'november': 'Nov',
         'december': 'Dec',
      }

      if isinstance( month, int ):
         if month not in month_map:
            raise ValueError( f'Invalid month: { month }' )
         return month_map[ month ]

      if isinstance( month, str ):
         month = month.strip()

         if month.isdigit():
            month_num = int( month )
            if month_num not in month_map:
               raise ValueError( f'Invalid month: { month }' )
            return month_map[ month_num ]

         lowered = month.lower()

         if lowered in full_name_map:
            return full_name_map[ lowered ]

         abbrev = month[ :3 ].title()
         if abbrev in month_map.values():
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
      month_index = {
         'JAN': 0,
         'FEB': 1,
         'MAR': 2,
         'APR': 3,
         'MAY': 4,
         'JUN': 5,
         'JUL': 6,
         'AUG': 7,
         'SEP': 8,
         'OCT': 9,
         'NOV': 10,
         'DEC': 11
      }

      days_in_month = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

      doy = sum( days_in_month[ :month_index[ month ] ] )
      return doy + ( day - 1 )


   @staticmethod
   def get_next_month( month: str ) -> str | None:
      if month in ( 'JAN', 'Jan' ):
         return 'Feb'
      elif month in ( 'FEB', 'Feb' ):
         return 'Mar'
      elif month in ( 'MAR', 'Mar' ):
         return 'Apr'
      elif month in ( 'APR', 'Apr' ):
         return 'May'
      elif month in ( 'MAY', 'May' ):
         return 'Jun'
      elif month in ( 'JUN', 'Jun' ):
         return 'Jul'
      elif month in ( 'JUL', 'Jul' ):
         return 'Aug'
      elif month in ( 'AUG', 'Aug' ):
         return 'Sep'
      elif month in ( 'SEP', 'Sep' ):
         return 'Oct'
      elif month in ( 'OCT', 'Oct' ):
         return 'Nov'
      elif month in ( 'NOV', 'Nov' ):
         return 'Dec'
      elif month in ( 'DEC', 'Dec' ):
         return 'Jan'

      return None


   @staticmethod
   def get_number_of_days_in_month( month: str ) -> int | None:
      if month in ( 'JAN', 'Jan', 'MAR', 'Mar', 'MAY', 'May', 'JUL', 'Jul', 'AUG', 'Aug', 'OCT', 'Oct', 'DEC', 'Dec' ):
         return 31
      elif month in ( 'APR', 'Apr', 'JUN', 'Jun', 'SEP', 'Sep', 'NOV', 'Nov' ):
         return 30
      elif month in ( 'FEB', 'Feb' ):
         return 28

      return None


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
