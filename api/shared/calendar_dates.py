from __future__ import annotations

from collections.abc import Sequence
from datetime import date, datetime, time, timedelta
from typing import Any

from ..models.date_range import DateRange
from ..types import DateInput, DateKey, MonthInput, TimeInput, VisitDay, VisitMonth, VisitYear


class DateValues:
   @staticmethod
   def parse_datetime_value( value: str | None ) -> datetime | None:
      if value == None:
         return None

      for fmt in (
         '%Y-%m-%d %I:%M %p',
         '%Y-%m-%d %H:%M:%S',
         '%Y-%m-%d %H:%M'
      ):

         try:
            return datetime.strptime( value, fmt )
         except ValueError:
            pass

      raise ValueError( f'Unsupported datetime format: { value }' )


   @staticmethod
   def parse_time_value( value: TimeInput ) -> time | None:
      if value == None:
         return None

      if isinstance( value, datetime ):
         return value.time().replace( microsecond=0 )

      if isinstance( value, time ):
         return value.replace( microsecond=0 )

      value = str( value ).strip()

      if not value:
         return None

      for fmt in (
         '%H:%M:%S',
         '%H:%M',
         '%I:%M %p',
         '%I:%M:%S %p',
      ):

         try:
            return datetime.strptime( value, fmt ).time()
         except ValueError:
            pass

      raise ValueError( f'Unsupported time format: { value }' )


   @staticmethod
   def format_time_value( value: TimeInput ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      if parsed_time.second == 0:
         return parsed_time.strftime( '%H:%M' )

      return parsed_time.strftime( '%H:%M:%S' )


   @staticmethod
   def format_display_time_value( value: TimeInput ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      if parsed_time.second == 0:
         return parsed_time.strftime( '%I:%M %p' ).lstrip( '0' )

      return parsed_time.strftime( '%I:%M:%S %p' ).lstrip( '0' )


   @staticmethod
   def time_value_in_seconds( value: TimeInput ) -> int | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      return (
         ( parsed_time.hour * 3600 )
         + ( parsed_time.minute * 60 )
         + parsed_time.second )


   @staticmethod
   def time_value_is_before(
         left: TimeInput,
         right: TimeInput ) -> bool:
      left_seconds = DateValues.time_value_in_seconds( left )
      right_seconds = DateValues.time_value_in_seconds( right )

      return (
         left_seconds is not None
         and right_seconds is not None
         and left_seconds < right_seconds )


   @staticmethod
   def time_value_is_after(
         left: TimeInput,
         right: TimeInput ) -> bool:
      left_seconds = DateValues.time_value_in_seconds( left )
      right_seconds = DateValues.time_value_in_seconds( right )

      return (
         left_seconds is not None
         and right_seconds is not None
         and left_seconds > right_seconds )


   @staticmethod
   def time_value_in_minutes( value: TimeInput ) -> int | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      return ( parsed_time.hour * 60 ) + parsed_time.minute


   @staticmethod
   def schedule_time_key_from_seconds( total_seconds: int ) -> str:
      hours = total_seconds // 3600
      minutes = ( total_seconds % 3600 ) // 60
      seconds = total_seconds % 60

      time_value = time(
         hour=hours,
         minute=minutes,
         second=seconds )
      formatted = DateValues.format_display_time_value( time_value )

      if formatted == None:
         raise ValueError( f'Invalid schedule time seconds: { total_seconds }' )

      return formatted


   @staticmethod
   def schedule_time_key_from_minutes( minutes: int ) -> str:
      hours = minutes // 60
      minute_value = minutes % 60
      formatted = DateValues.format_display_time_value(
         time( hour=hours, minute=minute_value ) )

      if formatted == None:
         raise ValueError( f'Invalid schedule time minutes: { minutes }' )

      return formatted


   @staticmethod
   def add_minutes_to_time( value: TimeInput, minutes: int | None ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None or minutes == None:
         return None

      duration = int( minutes )

      if duration <= 0:
         return None

      anchor = datetime.combine( date.today(), parsed_time )
      result_time = ( anchor + timedelta( minutes=duration ) ).time()
      return DateValues.format_display_time_value( result_time )


   @staticmethod
   def parse_date_value( value: DateInput ) -> date | None:
      if value == None:
         return None

      if isinstance( value, date ) and not isinstance( value, datetime ):
         return value

      if isinstance( value, datetime ):
         return value.date()

      value = str( value ).strip()

      try:
         return date.fromisoformat( value )
      except ValueError:
         pass

      date_part = value.split( ' ' )[ 0 ]

      try:
         return date.fromisoformat( date_part )
      except ValueError:
         pass

      raise ValueError( f'Unsupported date format: { value }' )


   @staticmethod
   def normalize_date_key( value: DateInput ) -> DateKey | None:
      if value == None:
         return None

      if isinstance( value, str ) and value.strip() == '':
         return None

      try:
         parsed = DateValues.parse_date_value( value )
      except ValueError:
         return None

      if parsed == None:
         return None

      return parsed.isoformat()


   @staticmethod
   def today_date_key() -> DateKey:
      return datetime.now().date().isoformat()


   @staticmethod
   def resolve_open_ended_date_range(
         start_date: DateInput,
         end_date: DateInput ) -> DateRange:
      if not start_date:
         start_date = DateValues.today_date_key()

      return DateRange(
         start_date=DateValues.normalize_date_key( start_date ),
         end_date=DateValues.normalize_date_key( end_date ) )


   @staticmethod
   def format_display_date_value( value: DateInput ) -> str | None:
      parsed_date = DateValues.parse_date_value( value )

      if parsed_date == None:
         return None

      return f'{ parsed_date.strftime( "%B" ) } { parsed_date.day }, { parsed_date.year }'


   @staticmethod
   def normalize_schedule_time_key( value: TimeInput ) -> str:
      return str( value or '' ).strip()


   @staticmethod
   def normalize_schedule_time( value: TimeInput ) -> str | None:
      if value == None:
         return None

      try:
         return DateValues.format_display_time_value( value )
      except ValueError:
         return None


   @staticmethod
   def normalize_unique_schedule_times(
         values: Sequence[ TimeInput ] ) -> list[ str ]:
      unique_times: list[ str ] = []
      seen_seconds: set[ int ] = set()

      for value in values:
         normalized_time = DateValues.normalize_schedule_time( value )
         time_seconds = DateValues.time_value_in_seconds( normalized_time )

         if (
            normalized_time == None
            or time_seconds == None
            or time_seconds in seen_seconds
         ):
            continue

         seen_seconds.add( time_seconds )
         unique_times.append( normalized_time )

      return unique_times


   @staticmethod
   def normalize_itinerary_schedule_time( value: TimeInput ) -> str | None:
      return DateValues.normalize_schedule_time( value )


   @staticmethod
   def normalize_unique_itinerary_schedule_times(
         values: Sequence[ TimeInput ] ) -> list[ str ]:
      return DateValues.normalize_unique_schedule_times( values )


   @staticmethod
   def is_date_on_or_after( date_value: DateInput, boundary_value: DateInput ) -> bool:
      if boundary_value is None:
         return True

      return DateValues.parse_date_value( date_value ) >= DateValues.parse_date_value( boundary_value )


   @staticmethod
   def is_date_on_or_before( date_value: DateInput, boundary_value: DateInput ) -> bool:
      if boundary_value is None:
         return True

      return DateValues.parse_date_value( date_value ) <= DateValues.parse_date_value( boundary_value )


   @staticmethod
   def is_date_in_range(
         target_date: DateInput,
         start_date_value: DateInput,
         end_date_value: DateInput ) -> bool:
      return (
         DateValues.is_date_on_or_after( target_date, start_date_value )
         and DateValues.is_date_on_or_before( target_date, end_date_value )
      )


   @staticmethod
   def is_date_range_ordered( start_date_value: DateInput, end_date_value: DateInput ) -> bool:
      if end_date_value is None:
         return True

      return DateValues.parse_date_value( end_date_value ) >= DateValues.parse_date_value( start_date_value )


class CalendarDates:
   @staticmethod
   def normalize_month( month: MonthInput ) -> VisitMonth | None:
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
   def get_month_abbreviation( month: MonthInput ) -> str:
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
   def resolve_visit_calendar_month( month: MonthInput ) -> VisitMonth:
      label = CalendarDates.get_month_abbreviation( month )
      index = CalendarDates.normalize_month( month=label )

      if index is None:
         raise ValueError( f'Invalid month: { repr( month ) }' )

      return index


   @staticmethod
   def resolve_visit_day_of_month( day: VisitDay | str ) -> VisitDay:
      return int( day )


   @staticmethod
   def resolve_visit_calendar_year( calendar_year: VisitYear | None = None ) -> VisitYear:
      if calendar_year is not None:
         return int( calendar_year )

      return DateValues.parse_date_value( DateValues.today_date_key() ).year


   @staticmethod
   def visit_target_date( month: MonthInput, day: VisitDay | str, year: VisitYear | None ) -> date:
      return date(
         int( CalendarDates.resolve_visit_calendar_year( year ) ),
         int( CalendarDates.resolve_visit_calendar_month( month ) ),
         int( CalendarDates.resolve_visit_day_of_month( day ) ),
      )


   @staticmethod
   def schedule_includes_weekday( weekday_index: int, monday_through_sunday: Sequence[ Any ] ) -> bool:
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
   def is_peak_season_month( month: MonthInput ) -> bool:
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
   def get_family_day( year: VisitYear ) -> date:
      d = date( year, 2, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=14 )


   @staticmethod
   def get_good_friday( year: VisitYear ) -> date:
      easter = CalendarDates.get_easter_date( year )
      return easter - timedelta( days=2 )


   @staticmethod
   def get_easter_date( year: VisitYear ) -> date:
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
   def get_victoria_day( year: VisitYear ) -> date:
      d = date( year, 5, 24 )

      while d.weekday() != 0:
         d -= timedelta( days=1 )

      return d


   @staticmethod
   def get_civic_holiday( year: VisitYear ) -> date:
      d = date( year, 8, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_labour_day( year: VisitYear ) -> date:
      d = date( year, 9, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_thanksgiving( year: VisitYear ) -> date:
      d = date( year, 10, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=7 )
