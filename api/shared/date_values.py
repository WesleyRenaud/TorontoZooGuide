from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any

from ..models.date_range import DateRange
from ..types import Types


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
   def parse_time_value( value: Types.TimeInput ) -> time | None:
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
   def format_time_value( value: Types.TimeInput ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      if parsed_time.second == 0:
         return parsed_time.strftime( '%H:%M' )

      return parsed_time.strftime( '%H:%M:%S' )


   @staticmethod
   def format_display_time_value( value: Types.TimeInput ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      if parsed_time.second == 0:
         return parsed_time.strftime( '%I:%M %p' ).lstrip( '0' )

      return parsed_time.strftime( '%I:%M:%S %p' ).lstrip( '0' )


   @staticmethod
   def time_value_in_seconds( value: Types.TimeInput ) -> int | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      return (
         ( parsed_time.hour * 3600 )
         + ( parsed_time.minute * 60 )
         + parsed_time.second )


   @staticmethod
   def time_value_is_before(
         left: Types.TimeInput,
         right: Types.TimeInput ) -> bool:
      left_seconds = DateValues.time_value_in_seconds( left )
      right_seconds = DateValues.time_value_in_seconds( right )

      return (
         left_seconds is not None
         and right_seconds is not None
         and left_seconds < right_seconds )


   @staticmethod
   def time_value_is_after(
         left: Types.TimeInput,
         right: Types.TimeInput ) -> bool:
      left_seconds = DateValues.time_value_in_seconds( left )
      right_seconds = DateValues.time_value_in_seconds( right )

      return (
         left_seconds is not None
         and right_seconds is not None
         and left_seconds > right_seconds )


   @staticmethod
   def time_value_is_at_or_after(
         left: Types.TimeInput,
         right: Types.TimeInput ) -> bool:
      left_seconds = DateValues.time_value_in_seconds( left )
      right_seconds = DateValues.time_value_in_seconds( right )

      return (
         left_seconds is not None
         and right_seconds is not None
         and left_seconds >= right_seconds )


   @staticmethod
   def time_value_in_minutes( value: Types.TimeInput ) -> int | None:
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
   def add_minutes_to_time( value: Types.TimeInput, minutes: int | None ) -> str | None:
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
   def parse_date_value( value: Types.DateInput ) -> date | None:
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
   def normalize_date_key( value: Types.DateInput ) -> Types.DateKey | None:
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
   def today_date_key() -> Types.DateKey:
      return datetime.now().date().isoformat()


   @staticmethod
   def resolve_open_ended_date_range(
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> DateRange:
      if not start_date:
         start_date = DateValues.today_date_key()

      return DateRange(
         start_date=DateValues.normalize_date_key( start_date ),
         end_date=DateValues.normalize_date_key( end_date ) )


   @staticmethod
   def format_display_date_value( value: Types.DateInput ) -> str | None:
      parsed_date = DateValues.parse_date_value( value )

      if parsed_date == None:
         return None

      return f'{ parsed_date.strftime( "%B" ) } { parsed_date.day }, { parsed_date.year }'


   @staticmethod
   def normalize_schedule_time_key( value: Types.TimeInput ) -> str:
      return str( value or '' ).strip()


   @staticmethod
   def normalize_schedule_time( value: Types.TimeInput ) -> str | None:
      if value == None:
         return None

      try:
         return DateValues.format_display_time_value( value )
      except ValueError:
         return None


   @staticmethod
   def normalize_unique_schedule_times(
         values: list[ Types.TimeInput ] ) -> list[ str ]:
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
   def normalize_itinerary_schedule_time( value: Types.TimeInput ) -> str | None:
      return DateValues.normalize_schedule_time( value )


   @staticmethod
   def normalize_unique_itinerary_schedule_times(
         values: list[ Types.TimeInput ] ) -> list[ str ]:
      return DateValues.normalize_unique_schedule_times( values )


   @staticmethod
   def is_date_on_or_after( date_value: Types.DateInput, boundary_value: Types.DateInput ) -> bool:
      if boundary_value is None:
         return True

      return DateValues.parse_date_value( date_value ) >= DateValues.parse_date_value( boundary_value )


   @staticmethod
   def is_date_on_or_before( date_value: Types.DateInput, boundary_value: Types.DateInput ) -> bool:
      if boundary_value is None:
         return True

      return DateValues.parse_date_value( date_value ) <= DateValues.parse_date_value( boundary_value )


   @staticmethod
   def is_date_in_range(
         target_date: Types.DateInput,
         start_date_value: Types.DateInput,
         end_date_value: Types.DateInput ) -> bool:
      return (
         DateValues.is_date_on_or_after( target_date, start_date_value )
         and DateValues.is_date_on_or_before( target_date, end_date_value )
      )


   @staticmethod
   def is_date_range_ordered( start_date_value: Types.DateInput, end_date_value: Types.DateInput ) -> bool:
      if end_date_value is None:
         return True

      return DateValues.parse_date_value( end_date_value ) >= DateValues.parse_date_value( start_date_value )
