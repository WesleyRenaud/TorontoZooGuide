from __future__ import annotations

import calendar
from datetime import date
from datetime import timedelta
from html import unescape
import re

from api.app_string_provider import AppStringProvider
from api.models import ZooHours
from api.shared.calendar_dates import CalendarDates
from .date_patterns import DatePatterns
from .date_span import DateSpan


class ZooHoursPage():
   WEEKDAYS = {
      name.casefold(): index
      for index, name in enumerate( calendar.day_name )
   }
   TIME_RANGE_RE = re.compile(
      r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*[-–—]\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)',
      re.IGNORECASE,
   )
   LAST_ADMISSION_RE = re.compile(
      r'(?i)last admission\s+(?:(\d+)\s+hours?\s+before\s+clos(?:e|ing)|'
      r'(\d{1,2})(?::(\d{2}))?\s*(am|pm))'
   )


   @classmethod
   def parse_clock( cls, hour: str, minute: str | None, ampm: str ) -> str:
      parsed_hour = int( hour )
      parsed_minute = 0 if minute == None else int( minute )
      meridian = ampm.casefold()

      if meridian == 'pm' and parsed_hour != 12:
         parsed_hour += 12

      if meridian == 'am' and parsed_hour == 12:
         parsed_hour = 0

      return f'{ str( parsed_hour ).zfill( 2 ) }:{ str( parsed_minute ).zfill( 2 ) }'


   @classmethod
   def subtract_hours( cls, clock: str, hours: int ) -> str:
      hour, minute = ( int( part ) for part in clock.split( ':' ) )
      total = hour * 60 + minute - hours * 60

      if total < 0:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageLastAdmissionBeforeMidnight' ) )

      return f'{ str( total // 60 ).zfill( 2 ) }:{ str( total % 60 ).zfill( 2 ) }'


   @classmethod
   def hours_lines( cls, page_html: str ) -> list[ str ]:
      marker = page_html.casefold().find( 'id="currenthours"' )

      if marker < 0:
         marker = page_html.casefold().find( 'id="allhours"' )

      if marker < 0:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursList' ) )

      paragraph = re.search( r'(?is)<p\b[^>]*>(.*?)</p>', page_html[ marker: ] )

      if paragraph == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursList' ) )

      text = re.sub( r'(?is)<br\s*/?>', '\n', paragraph.group( 1 ) )
      text = re.sub( r'<[^>]+>', '', text )
      text = unescape( text ).replace( '\xa0', ' ' )
      lines = []

      for line in text.splitlines():
         cleaned = re.sub( r'\s+', ' ', line ).strip( ' *' )

         if cleaned:
            lines.append( cleaned )

      if not lines:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursList' ) )

      return lines


   @classmethod
   def parse_named_date( cls, text: str ) -> date | None:
      match = DatePatterns.DATE_RE.search( text )

      if match == None:
         return None

      month = CalendarDates.month_index( match.group( 'month' ) )

      if month == None:
         return None

      try:
         return date( int( match.group( 'year' ) ), month, int( match.group( 'day' ) ) )
      except ValueError:
         return None


   @classmethod
   def parse_range( cls, line: str, today: date ) -> DateSpan:
      parts = re.split( r'(?i)\bthrough\b', line, maxsplit=1 )

      if len( parts ) != 2:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursRange' ) )

      end = cls.parse_named_date( parts[ 1 ] )

      if end == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursRange' ) )

      if re.search( r'(?i)\b(?:now|today)\b', parts[ 0 ] ):
         start = today
      else:
         start = cls.parse_named_date( parts[ 0 ] )

      if start == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursRange' ) )

      if end < start:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageHoursRangeEndsBeforeStart' ) )

      return DateSpan( start=start, end=end )


   @classmethod
   def last_admission_clock( cls, line: str, close: str ) -> str | None:
      match = cls.LAST_ADMISSION_RE.search( line )

      if match == None:
         return None

      if match.group( 1 ) != None:
         return cls.subtract_hours( close, int( match.group( 1 ) ) )

      return cls.parse_clock( match.group( 2 ), match.group( 3 ), match.group( 4 ) )


   @classmethod
   def weekday_index( cls, line: str ) -> int | None:
      for name, index in cls.WEEKDAYS.items():
         if re.search( rf'(?i)\b{ name }\b', line ):
            return index

      return None


   @classmethod
   def exception_dates( cls, line: str, span: DateSpan ) -> list[ date ]:
      named = cls.parse_named_date( line )

      if named != None:
         dates = [ named ]
      else:
         match = DatePatterns.MONTH_DAY_RE.search( line )
         month = None if match == None else CalendarDates.month_index( match.group( 'month' ) )

         if month == None:
            raise RuntimeError( AppStringProvider.format( 'checks.planPageExceptionWithoutDate' ) )

         day = int( match.group( 'day' ) )
         dates = []

         for year in range( span.start.year, span.end.year + 1 ):
            try:
               candidate = date( year, month, day )
            except ValueError:
               continue

            if span.start <= candidate <= span.end:
               dates.append( candidate )

      weekday = cls.weekday_index( line )

      if weekday != None:
         dates = [ candidate for candidate in dates if candidate.weekday() == weekday ]

      if not dates:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageExceptionOutsideRange' ) )

      return dates


   @classmethod
   def each_day( cls, span: DateSpan ) -> list[ date ]:
      days = []
      day = span.start

      while day <= span.end:
         days.append( day )
         day += timedelta( days=1 )

      return days


   @classmethod
   def day_hours(
         cls,
         day: date,
         open_time: str,
         last_admission: str,
         close_time: str ) -> ZooHours:
      return ZooHours(
         date=day.isoformat(),
         early_admission_time=None,
         open_time=open_time,
         last_admission_time=last_admission,
         close_time=close_time,
      )


   @classmethod
   def hours_on_day( cls, day: date, line: str, admission_lines: list[ str ] ) -> ZooHours:
      match = cls.TIME_RANGE_RE.search( line )

      if match == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoDailyHours' ) )

      open_time = cls.parse_clock( match.group( 1 ), match.group( 2 ), match.group( 3 ) )
      close_time = cls.parse_clock( match.group( 4 ), match.group( 5 ), match.group( 6 ) )
      admission = None

      for admission_line in admission_lines:
         admission = cls.last_admission_clock( admission_line, close_time )

         if admission != None:
            break

      if admission == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoLastAdmission' ) )

      return cls.day_hours( day, open_time, admission, close_time )


   @classmethod
   def replace_day( cls, hours: list[ ZooHours ], updated: ZooHours ) -> list[ ZooHours ]:
      return [
         updated if item.date == updated.date else item
         for item in hours
      ]


   @classmethod
   def parse( cls, page_html: str, today: date ) -> list[ ZooHours ]:
      lines = cls.hours_lines( page_html )
      range_line = next( ( line for line in lines if 'through' in line.casefold() ), None )
      daily_line = next( ( line for line in lines if line.casefold().startswith( 'daily' ) ), None )
      footnote = next( ( line for line in lines if 'last admission' in line.casefold() ), None )

      if range_line == None or daily_line == None or footnote == None:
         raise RuntimeError( AppStringProvider.format( 'checks.planPageNoHoursList' ) )

      span = cls.parse_range( range_line, today )
      hours = [
         cls.hours_on_day( day, daily_line, [ footnote ] )
         for day in cls.each_day( span )
      ]

      for line in lines:
         if line == range_line or line == daily_line or 'last admission' in line.casefold():
            continue

         if cls.TIME_RANGE_RE.search( line ) == None:
            continue

         for day in cls.exception_dates( line, span ):
            hours = cls.replace_day( hours, cls.hours_on_day( day, line, [ line, footnote ] ) )

      return hours
