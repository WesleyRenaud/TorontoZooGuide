from __future__ import annotations

import argparse
import calendar
from datetime import date
from datetime import timedelta
from html import unescape
from pathlib import Path
import re
import sqlite3
import sys

from tools.seasonalOffDisplayCheck import fetch_text


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_PLAN_URL = 'https://www.torontozoo.com/plan'
WEEKDAYS = {
   name.casefold(): index
   for index, name in enumerate( calendar.day_name )
}
MONTHS = {
   name.casefold(): index
   for index, name in enumerate( calendar.month_name )
   if name
}
TIME_RANGE_RE = re.compile(
   r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*[-–—]\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)',
   re.IGNORECASE,
)
LAST_ADMISSION_RE = re.compile(
   r'(?i)last admission\s+(?:(\d+)\s+hours?\s+before\s+clos(?:e|ing)|'
   r'(\d{1,2})(?::(\d{2}))?\s*(am|pm))'
)
DATE_RE = re.compile(
   r'(?i)([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})'
)
MONTH_DAY_RE = re.compile(
   r'(?i)([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?'
)
Hours = tuple[ str | None, str, str, str ]


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare zoo hours listed on the Toronto Zoo website with the zoo '
         'hours in the app.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def parse_clock( hour: str, minute: str | None, ampm: str ) -> str:
   parsed_hour = int( hour )
   parsed_minute = 0 if minute == None else int( minute )
   meridian = ampm.casefold()

   if meridian == 'pm' and parsed_hour != 12:
      parsed_hour += 12

   if meridian == 'am' and parsed_hour == 12:
      parsed_hour = 0

   return f'{ str( parsed_hour ).zfill( 2 ) }:{ str( parsed_minute ).zfill( 2 ) }'


def parse_time_range( line: str ) -> tuple[ str, str ] | None:
   match = TIME_RANGE_RE.search( line )

   if match == None:
      return None

   return (
      parse_clock( match.group( 1 ), match.group( 2 ), match.group( 3 ) ),
      parse_clock( match.group( 4 ), match.group( 5 ), match.group( 6 ) ),
   )


def subtract_hours( clock: str, hours: int ) -> str:
   hour, minute = ( int( part ) for part in clock.split( ':' ) )
   total = hour * 60 + minute - hours * 60

   if total < 0:
      raise RuntimeError( 'The plan page last admission is before midnight.' )

   return f'{ str( total // 60 ).zfill( 2 ) }:{ str( total % 60 ).zfill( 2 ) }'


def hours_lines( page_html: str ) -> list[ str ]:
   marker = page_html.casefold().find( 'id="currenthours"' )

   if marker < 0:
      marker = page_html.casefold().find( 'id="allhours"' )

   if marker < 0:
      raise RuntimeError( 'The plan page has no hours list.' )

   paragraph = re.search( r'(?is)<p\b[^>]*>(.*?)</p>', page_html[ marker: ] )

   if paragraph == None:
      raise RuntimeError( 'The plan page has no hours list.' )

   text = re.sub( r'(?is)<br\s*/?>', '\n', paragraph.group( 1 ) )
   text = re.sub( r'<[^>]+>', '', text )
   text = unescape( text ).replace( '\xa0', ' ' )
   lines = []

   for line in text.splitlines():
      cleaned = re.sub( r'\s+', ' ', line ).strip( ' *' )

      if cleaned:
         lines.append( cleaned )

   if not lines:
      raise RuntimeError( 'The plan page has no hours list.' )

   return lines


def parse_named_date( text: str ) -> date | None:
   match = DATE_RE.search( text )

   if match == None:
      return None

   month = MONTHS.get( match.group( 1 ).casefold() )

   if month == None:
      return None

   try:
      return date( int( match.group( 3 ) ), month, int( match.group( 2 ) ) )
   except ValueError:
      return None


def parse_range( line: str, today: date ) -> tuple[ date, date ]:
   parts = re.split( r'(?i)\bthrough\b', line, maxsplit=1 )

   if len( parts ) != 2:
      raise RuntimeError( 'The plan page has no hours range.' )

   end = parse_named_date( parts[ 1 ] )

   if end == None:
      raise RuntimeError( 'The plan page has no hours range.' )

   if re.search( r'(?i)\b(?:now|today)\b', parts[ 0 ] ):
      start = today
   else:
      start = parse_named_date( parts[ 0 ] )

   if start == None:
      raise RuntimeError( 'The plan page has no hours range.' )

   if end < start:
      raise RuntimeError( 'The plan page hours range ends before it starts.' )

   return start, end


def last_admission_clock( line: str, close: str ) -> str | None:
   match = LAST_ADMISSION_RE.search( line )

   if match == None:
      return None

   if match.group( 1 ) != None:
      return subtract_hours( close, int( match.group( 1 ) ) )

   return parse_clock( match.group( 2 ), match.group( 3 ), match.group( 4 ) )


def weekday_index( line: str ) -> int | None:
   for name, index in WEEKDAYS.items():
      if re.search( rf'(?i)\b{ name }\b', line ):
         return index

   return None


def exception_dates(
      line: str,
      start: date,
      end: date ) -> list[ date ]:
   named = parse_named_date( line )

   if named != None:
      dates = [ named ]
   else:
      match = MONTH_DAY_RE.search( line )

      if match == None or MONTHS.get( match.group( 1 ).casefold() ) == None:
         raise RuntimeError( 'The plan page has an hours exception without a date.' )

      month = MONTHS[ match.group( 1 ).casefold() ]
      day = int( match.group( 2 ) )
      dates = []

      for year in range( start.year, end.year + 1 ):
         try:
            candidate = date( year, month, day )
         except ValueError:
            continue

         if start <= candidate <= end:
            dates.append( candidate )

   weekday = weekday_index( line )

   if weekday != None:
      dates = [ candidate for candidate in dates if candidate.weekday() == weekday ]

   if not dates:
      raise RuntimeError( 'The plan page hours exception is outside the published range.' )

   return dates


def each_day( start: date, end: date ) -> list[ date ]:
   days = []
   day = start

   while day <= end:
      days.append( day )
      day += timedelta( days=1 )

   return days


def parse_website_hours( page_html: str, today: date ) -> dict[ date, Hours ]:
   lines = hours_lines( page_html )
   range_line = next( ( line for line in lines if 'through' in line.casefold() ), None )
   daily_line = next( ( line for line in lines if line.casefold().startswith( 'daily' ) ), None )
   footnote = next( ( line for line in lines if 'last admission' in line.casefold() ), None )

   if range_line == None or daily_line == None or footnote == None:
      raise RuntimeError( 'The plan page has no hours list.' )

   start, end = parse_range( range_line, today )
   daily_range = parse_time_range( daily_line )

   if daily_range == None:
      raise RuntimeError( 'The plan page has no daily hours.' )

   open_time, close_time = daily_range
   admission = last_admission_clock( footnote, close_time )

   if admission == None:
      raise RuntimeError( 'The plan page has no last admission time.' )

   hours = {
      day: ( None, open_time, admission, close_time )
      for day in each_day( start, end )
   }

   for line in lines:
      if line == range_line or line == daily_line or 'last admission' in line.casefold():
         continue

      exception_range = parse_time_range( line )

      if exception_range == None:
         continue

      exception_open, exception_close = exception_range
      exception_admission = last_admission_clock( line, exception_close )

      if exception_admission == None:
         exception_admission = last_admission_clock( footnote, exception_close )

      if exception_admission == None:
         raise RuntimeError( 'The plan page has no last admission time.' )

      for day in exception_dates( line, start, end ):
         hours[ day ] = ( None, exception_open, exception_admission, exception_close )

   return hours


def fetch_website_hours( today: date ) -> dict[ date, Hours ]:
   return parse_website_hours( fetch_text( WEBSITE_PLAN_URL ), today )


def load_hours( database: Path ) -> dict[ date, Hours ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      rows = connection.execute(
         """   SELECT
                  OPERATING_DATE,
                  EARLY_ADMISSION_TIME,
                  OPEN_TIME,
                  LAST_ADMISSION_TIME,
                  CLOSE_TIME
               FROM ZooHours
               ORDER BY OPERATING_DATE
         """
      ).fetchall()
   finally:
      connection.close()

   hours = {}

   for operating_date, early, open_time, last_admission, close in rows:
      hours[ date.fromisoformat( str( operating_date ) ) ] = (
         None if early == None else str( early ),
         str( open_time ),
         str( last_admission ),
         str( close ),
      )

   return hours


def format_hours( hours: Hours ) -> str:
   early, open_time, last_admission, close = hours
   parts = []

   if early != None:
      parts.append( f'early admission { early }' )

   parts.append( f'open { open_time }' )
   parts.append( f'last admission { last_admission }' )
   parts.append( f'close { close }' )
   return ', '.join( parts )


def group_days( days: list[ tuple[ date, Hours ] ] ) -> list[ tuple[ date, date, Hours ] ]:
   groups = []

   for day, hours in days:
      if groups and groups[ -1 ][ 1 ] + timedelta( days=1 ) == day and groups[ -1 ][ 2 ] == hours:
         groups[ -1 ] = ( groups[ -1 ][ 0 ], day, hours )
         continue

      groups.append( ( day, day, hours ) )

   return groups


def format_group( start: date, end: date, hours: Hours ) -> str:
   if start == end:
      return f'{ start.isoformat() }: { format_hours( hours ) }'

   days = ( end - start ).days + 1
   return f'{ start.isoformat() } to { end.isoformat() } ({ days } days): { format_hours( hours ) }'


def print_category( title: str, days: list[ tuple[ date, Hours ] ] ) -> None:
   print( f'{ title }: { len( days ) }' )

   for start, end, hours in group_days( days ):
      print( f'  { format_group( start, end, hours ) }' )

   print()


def check_lists( database: Path, today: date ) -> int:
   app_hours = {
      day: hours
      for day, hours in load_hours( database ).items()
      if day >= today
   }
   website_hours = {
      day: hours
      for day, hours in fetch_website_hours( today ).items()
      if day >= today
   }
   website_only = []
   app_only = []

   for day in sorted( set( website_hours ) | set( app_hours ) ):
      website = website_hours.get( day )
      app = app_hours.get( day )

      if website == app:
         continue

      if website != None:
         website_only.append( ( day, website ) )

      if app != None:
         app_only.append( ( day, app ) )

   print( f'Zoo hours check for { today.isoformat() }.' )
   print()
   print_category( 'On the website and not in the app', website_only )
   print_category( 'In the app and not on the website', app_only )

   return len( website_only ) + len( app_only )


def main() -> int:
   args = parse_args()

   if not args.database.exists():
      print( f'Could not find { args.database }.', file=sys.stderr )
      return 2

   try:
      issues = check_lists( args.database, date.today() )
   except RuntimeError as error:
      print( error, file=sys.stderr )
      return 2

   if issues:
      return 1

   return 0


if __name__ == '__main__':
   raise SystemExit( main() )
