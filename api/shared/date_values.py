from __future__ import annotations

from datetime import date, datetime, time, timedelta

from ..models.date_range import DateRange
from ..types import DateInput, DateKey


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
   def parse_time_value( value: str | None ) -> time | None:
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
   def format_time_value( value: str | None ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      return parsed_time.strftime( '%H:%M' )


   @staticmethod
   def format_display_time_value( value: str | None ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None:
         return None

      return parsed_time.strftime( '%I:%M %p' ).lstrip( '0' )


   @staticmethod
   def add_minutes_to_time( value: str | None, minutes: int | None ) -> str | None:
      parsed_time = DateValues.parse_time_value( value )

      if parsed_time == None or minutes == None:
         return None

      duration = int( minutes )

      if duration <= 0:
         return None

      anchor = datetime.combine( date.today(), parsed_time )
      return ( anchor + timedelta( minutes=duration ) ).time().strftime( '%H:%M' )


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
   def normalize_itinerary_schedule_time( value: str | None ) -> str:
      if value == None:
         return ''

      return str( value ).strip()


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
