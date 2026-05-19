from datetime import date, datetime, timedelta
import calendar
import math
import sys


class ZooUtil:
   @staticmethod
   def parse_datetime_value( value ):
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
   def parse_time_value( value ):
      if value == None:
         return None

      value = str( value ).strip()

      if not value:
         return None

      for fmt in (
         '%H:%M',
         '%I:%M %p'
      ):

         try:
            return datetime.strptime( value, fmt ).time()
         except ValueError:
            pass

      raise ValueError( f'Unsupported time format: { value }' )


   @staticmethod
   def format_time_value( value ):
      parsed_time = ZooUtil.parse_time_value( value )

      if parsed_time == None:
         return None

      return parsed_time.strftime( '%H:%M' )


   @staticmethod
   def add_minutes_to_time( value, minutes ):
      parsed_time = ZooUtil.parse_time_value( value )

      if parsed_time == None or minutes == None:
         return None

      duration = int( minutes )

      if duration <= 0:
         return None

      anchor = datetime.combine( date.today(), parsed_time )
      return ( anchor + timedelta( minutes=duration ) ).time().strftime( '%H:%M' )


   @staticmethod
   def parse_date_value( value ):
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
   def normalize_date_key( value ):
      if value == None:
         return None

      if isinstance( value, str ) and value.strip() == '':
         return None

      try:
         parsed = ZooUtil.parse_date_value( value )
      except ValueError:
         return None

      if parsed == None:
         return None

      return parsed.isoformat()


   @staticmethod
   def normalize_itinerary_schedule_time( value ):
      if value == None:
         return ''

      return str( value ).strip()


   @staticmethod
   def is_date_on_or_after( date_value, boundary_value ):
      """True when ``date_value`` is on or after ``boundary_value``.

      A ``None`` ``boundary_value`` is treated as unbounded (always true).
      """
      if boundary_value is None:
         return True

      return ZooUtil.parse_date_value( date_value ) >= ZooUtil.parse_date_value( boundary_value )


   @staticmethod
   def is_date_on_or_before( date_value, boundary_value ):
      """True when ``date_value`` is on or before ``boundary_value``.

      A ``None`` ``boundary_value`` is treated as unbounded (always true).
      """
      if boundary_value is None:
         return True

      return ZooUtil.parse_date_value( date_value ) <= ZooUtil.parse_date_value( boundary_value )


   @staticmethod
   def is_date_in_range( target_date, start_date_value, end_date_value ):
      return (
         ZooUtil.is_date_on_or_after( target_date, start_date_value )
         and ZooUtil.is_date_on_or_before( target_date, end_date_value )
      )


   @staticmethod
   def as_boolean( value ):
      if isinstance( value, bool ):
         return value

      if isinstance( value, int ):
         return value != 0

      return False


   @staticmethod
   def get_average_temperature( month, day ):
      # Convert month/day to day-of-year
      month = ZooUtil.normalize_month( month )
      day_of_year = sum( calendar.monthrange( 2024, m )[ 1 ] for m in range( 1, month ) ) + day

      # Month start temperatures (°C)
      month_base = {
         1: -5.0,   # January
         2: -4.0,   # February
         3:  1.0,   # March
         4:  8.0,   # April
         5: 14.0,   # May
         6: 22.0,   # June
         7: 26.0,   # July
         8: 25.0,   # August
         9: 22.0,   # September
         10: 20.0,  # October
         11: 10.0,  # November
         12: 1.0    # December
      }

      # Compute start-of-month day-of-year mapping
      month_start_doy = []
      cumulative = 1
      for m in range( 1, 13 ):
         month_start_doy.append( ( cumulative, month_base[ m ] ) )
         cumulative += calendar.monthrange( 2024, m )[ 1 ]

      # Find which interval the day-of-year falls into
      for i in range( len( month_start_doy ) - 1 ):
         start_day, start_temp = month_start_doy[ i ]
         end_day, end_temp = month_start_doy[ i + 1 ]
         if start_day <= day_of_year < end_day:
            progress = ( day_of_year - start_day ) / ( end_day - start_day )
            temp = start_temp + ( end_temp - start_temp ) * progress
            return round( temp, 1 )

      # If day is in December
      temp = month_start_doy[ -1 ][ 1 ]
      return round( temp, 1 )


   @staticmethod
   def normalize_month( month ):
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
   def get_month_abbreviation( month ):
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
   def resolve_visit_calendar_month( month ):
      """API ``month`` (name, abbr, 1–12, ``'06'``-style string, etc.) -> ``int`` 1–12.

      Used for :class:`datetime.date` construction and SQL integer month columns.
      """
      label = ZooUtil.get_month_abbreviation( month )
      index = ZooUtil.normalize_month( month=label )

      if index is None:
         raise ValueError( f'Invalid month: { repr( month ) }' )

      return index


   @staticmethod
   def resolve_visit_day_of_month( day ):
      """API ``day`` value -> ``int`` day-of-month (same as ``int(day)``)."""
      return int( day )


   @staticmethod
   def resolve_visit_calendar_year( calendar_year=None ):
      """Calendar year for visit ``date`` construction. ``None`` uses the current local year."""
      if calendar_year is not None:
         return int( calendar_year )

      zoo_module = sys.modules.get( 'api.zoo' )
      datetime_class = getattr( zoo_module, 'datetime', datetime )
      return datetime_class.now().year


   @staticmethod
   def visit_target_date( month, day, year ):
      """Build a visit :class:`~datetime.date` from API ``month`` / ``day`` / ``year``."""
      return date(
         int( ZooUtil.resolve_visit_calendar_year( year ) ),
         int( ZooUtil.resolve_visit_calendar_month( month ) ),
         int( ZooUtil.resolve_visit_day_of_month( day ) ),
      )


   @staticmethod
   def schedule_includes_weekday( weekday_index, monday_through_sunday ):
      """Whether ``monday_through_sunday`` marks ``weekday_index`` as active.

      ``weekday_index`` follows :meth:`datetime.date.weekday` (Monday ``0`` through Sunday ``6``).
      ``monday_through_sunday`` is seven values in Monday-first order (truthy means scheduled).
      """
      if weekday_index < 0 or weekday_index > 6:
         return False

      return bool( monday_through_sunday[ weekday_index ] )


   @staticmethod
   def get_day_of_year( month, day ):
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
   def get_next_month( month ):
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


   @staticmethod
   def get_number_of_days_in_month( month ):
      if month in ( 'JAN', 'Jan', 'MAR', 'Mar', 'MAY', 'May', 'JUL', 'Jul', 'AUG', 'Aug', 'OCT', 'Oct', 'DEC', 'Dec' ):
         return 31
      elif month in ( 'APR', 'Apr', 'JUN', 'Jun', 'SEP', 'Sep', 'NOV', 'Nov' ):
         return 30
      elif month in ( 'FEB', 'Feb' ):
         return 28


   # Returns probability (between 0 and 1) that temperature is >= min_temperature, assuming a normal distribution N(mu, sigma)
   @staticmethod
   def get_temperature_probability( mu, sigma, min_temperature ):
      z = ( min_temperature - mu ) / sigma

      # Standard normal CDF via error function
      cdf = 0.5 * ( 1 + math.erf( z / math.sqrt( 2 ) ) )

      return round( 1.0 - cdf, 3 )


   @staticmethod
   def is_peak_season_month( month ):
      month = ZooUtil.normalize_month( month )

      if month >= 5 and month <= 10:
         return True

      return False


   @staticmethod
   def is_holiday( d ):
      year = d.year

      holidays = {
         date( year, 1, 1 ),               # New Year's Day
         ZooUtil.get_family_day( year ),
         ZooUtil.get_good_friday( year ),
         ZooUtil.get_victoria_day( year ),
         date( year, 7, 1 ),               # Canada Day
         ZooUtil.get_civic_holiday( year ),
         ZooUtil.get_labour_day( year ),
         ZooUtil.get_thanksgiving( year ),
         date( year, 12, 25 )              # Christmas Day
      }

      return d in holidays


   @staticmethod
   def get_family_day( year ):
      d = date( year, 2, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=14 )


   @staticmethod
   def get_good_friday( year ):
      easter = ZooUtil.get_easter_date( year )
      return easter - timedelta( days=2 )


   @staticmethod
   def get_easter_date( year ):
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
   def get_victoria_day( year ):
      d = date( year, 5, 24 )

      while d.weekday() != 0:
         d -= timedelta( days=1 )

      return d


   @staticmethod
   def get_civic_holiday( year ):
      d = date( year, 8, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_labour_day( year ):
      d = date( year, 9, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_thanksgiving( year ):
      d = date( year, 10, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=7 )
