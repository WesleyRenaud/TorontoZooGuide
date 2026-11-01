from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from html import unescape
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_SCHEDULE_URL = 'https://www.torontozoo.com/wildencounters'
BOOKING_GRAPHQL_URL = 'https://my.hornblower.com/graphql'
BOOKING_PROPERTY_ID = 'tozoo'
BOOKING_HORIZON_DAYS = 400
USER_AGENT = 'Mozilla/5.0'
WEEKDAY_LABELS = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
DISPLAY_WEEKDAYS = [ 6, 0, 1, 2, 3, 4, 5 ]
WEBSITE_WEEKDAYS = [ 6, 0, 1, 2, 3, 4, 5 ]
WEBSITE_NAME_ALIASES = {
   'bactrian camel': 'Bactrian Camels',
   'scales & tales': 'Scales & Tales of Americas',
   'snow leopard': 'Guardians of Snow Leopards',
   'the tiny tour!': 'The Tiny Tour',
}
ENABLED_DATES_QUERY = """
   query enabledDates(
      $propertyId: String!,
      $bookingType: String!,
      $correlationId: String!,
      $startDate: String!,
      $endDate: String! ) {
      enabledDates(
         propertyId: $propertyId,
         bookingType: $bookingType,
         correlationId: $correlationId,
         startDate: $startDate,
         endDate: $endDate ) {
         year
         months {
            month
            days
         }
      }
   }
"""


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare scheduled wild encounters with the Toronto Zoo website '
         'and each encounter booking calendar.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def curl( args: list[ str ], body: str | None = None ) -> str:
   result = subprocess.run(
      [
         'curl',
         '-fsS',
         '--max-time',
         '30',
         '-A',
         USER_AGENT,
         *args,
      ],
      input=None if body == None else body.encode(),
      check=False,
      capture_output=True,
   )

   if result.returncode != 0:
      detail = result.stderr.decode( errors='replace' ).strip()
      raise RuntimeError( detail or f'curl exited { result.returncode }' )

   return result.stdout.decode()


def fetch_text( url: str ) -> str:
   return curl( [ url ] )


def post_json( url: str, payload: dict[ str, object ] ) -> dict[ str, object ]:
   response = json.loads( curl(
      [
         '-H',
         'Content-Type: application/json',
         '--data-binary',
         '@-',
         url,
      ],
      json.dumps( payload ),
   ) )

   if not isinstance( response, dict ):
      raise RuntimeError( 'Booking calendar response was not an object.' )

   return response


def clean_cell( value: str ) -> str:
   text = re.sub( r'(?is)<[^>]+>', ' ', value )
   text = unescape( text ).replace( '\xa0', ' ' )
   return re.sub( r'\s+', ' ', text ).strip()


def format_clock( parsed: datetime ) -> str:
   hour = parsed.hour % 12 or 12
   minute = str( parsed.minute ).zfill( 2 )
   suffix = 'AM' if parsed.hour < 12 else 'PM'
   return f'{ hour }:{ minute } { suffix }'


def apply_website_meridiem( parsed: datetime ) -> datetime:
   if 1 <= parsed.hour <= 7:
      return parsed.replace( hour=parsed.hour + 12 )

   return parsed


def normalize_clock( value: str ) -> str:
   text = value.strip().upper()

   for pattern in ( '%I:%M %p', '%H:%M' ):
      try:
         parsed = datetime.strptime( text, pattern )
      except ValueError:
         continue

      if pattern == '%H:%M':
         parsed = apply_website_meridiem( parsed )

      return format_clock( parsed )

   return value.strip()


def clock_minutes( value: str ) -> int:
   try:
      parsed = datetime.strptime( value, '%I:%M %p' )
   except ValueError:
      return 0

   return parsed.hour * 60 + parsed.minute


def format_days( weekdays: set[ int ] ) -> str:
   return ', '.join(
      WEEKDAY_LABELS[ weekday ]
      for weekday in DISPLAY_WEEKDAYS
      if weekday in weekdays
   )


def describe_slots( slots: set[ tuple[ int, str ] ] ) -> str:
   by_time: dict[ str, set[ int ] ] = {}

   for weekday, encounter_time in slots:
      by_time.setdefault( encounter_time, set() ).add( weekday )

   descriptions = []

   for encounter_time in sorted( by_time, key=clock_minutes ):
      descriptions.append(
         f'{ encounter_time } { format_days( by_time[ encounter_time ] ) }'
      )

   return '; '.join( descriptions )


def parse_website_slots( page_html: str ) -> dict[ str, set[ tuple[ int, str ] ] ]:
   tables = re.findall( r'(?is)<table.*?</table>', page_html )

   if not tables:
      raise RuntimeError( 'The wild encounters page has no schedule table.' )

   slots: dict[ str, set[ tuple[ int, str ] ] ] = {}
   rows = re.findall( r'(?is)<tr.*?</tr>', tables[ 0 ] )

   for row in rows[ 1: ]:
      cells = [
         clean_cell( cell )
         for cell in re.findall( r'(?is)<t[dh][^>]*>(.*?)</t[dh]>', row )
      ]

      if len( cells ) < 8 or cells[ 0 ] == '':
         continue

      encounter_time = normalize_clock( cells[ 0 ] )

      for index, weekday in enumerate( WEBSITE_WEEKDAYS, start=1 ):
         name = cells[ index ]

         if name == '':
            continue

         slots.setdefault( name, set() ).add( ( weekday, encounter_time ) )

   if not slots:
      raise RuntimeError( 'The schedule table has no encounters.' )

   return slots


def resolve_website_name( name: str, app_names_by_fold: dict[ str, str ] ) -> str:
   alias = WEBSITE_NAME_ALIASES.get( name.casefold() )

   if alias != None:
      return app_names_by_fold.get( alias.casefold(), alias )

   return app_names_by_fold.get( name.casefold(), name )


def resolve_website_slots(
      website_slots: dict[ str, set[ tuple[ int, str ] ] ],
      app_names_by_fold: dict[ str, str ] ) -> dict[ str, set[ tuple[ int, str ] ] ]:
   resolved: dict[ str, set[ tuple[ int, str ] ] ] = {}

   for name, slots in website_slots.items():
      canonical_name = resolve_website_name( name, app_names_by_fold )
      resolved.setdefault( canonical_name, set() ).update( slots )

   return resolved


def parse_schedule_date( value: str | None ) -> date | None:
   if value == None or value == '':
      return None

   return date.fromisoformat( value )


def load_encounters(
      database: Path ) -> tuple[ dict[ str, str ], list[ tuple[ str, date, date | None, str, set[ int ] ] ] ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      link_rows = connection.execute(
         """   SELECT
                  NAME,
                  LINK
               FROM WildEncounter
         """
      ).fetchall()
      schedule_rows = connection.execute(
         """   SELECT
                  WILD_ENCOUNTER,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ENCOUNTER_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY
               FROM WildEncounterSchedule
         """
      ).fetchall()
   finally:
      connection.close()

   links = {
      str( name ): str( link )
      for name, link in link_rows
   }
   schedules = []

   for row in schedule_rows:
      weekdays = {
         index
         for index, flag in enumerate( row[ 4: ] )
         if flag
      }
      schedules.append( (
         str( row[ 0 ] ),
         date.fromisoformat( str( row[ 1 ] ) ),
         parse_schedule_date( None if row[ 2 ] == None else str( row[ 2 ] ) ),
         normalize_clock( str( row[ 3 ] ) ),
         weekdays,
      ) )

   return links, schedules


def active_slots(
      schedules: list[ tuple[ str, date, date | None, str, set[ int ] ] ],
      today: date ) -> dict[ str, set[ tuple[ int, str ] ] ]:
   slots: dict[ str, set[ tuple[ int, str ] ] ] = {}

   for name, start, end, encounter_time, weekdays in schedules:
      if start > today or ( end != None and end <= today ):
         continue

      for weekday in weekdays:
         slots.setdefault( name, set() ).add( ( weekday, encounter_time ) )

   return slots


def scheduled_dates(
      schedules: list[ tuple[ str, date, date | None, str, set[ int ] ] ],
      name: str,
      first: date,
      last: date ) -> list[ date ]:
   found: list[ date ] = []
   current = first

   while current <= last:
      weekday = current.weekday()

      for row_name, start, end, _encounter_time, weekdays in schedules:
         covers = start <= current and ( end == None or end > current )

         if row_name == name and covers and weekday in weekdays:
            found.append( current )
            break

      current += timedelta( days=1 )

   return found


def booking_type_id( page_html: str ) -> str | None:
   match = re.search( r'tour-id=["\'](\d+)["\']', page_html )

   if match == None:
      return None

   return match.group( 1 )


def booking_calendar_dates(
      booking_type: str,
      first: date,
      last: date ) -> list[ date ]:
   payload = post_json(
      BOOKING_GRAPHQL_URL,
      {
         'query': ENABLED_DATES_QUERY,
         'variables': {
            'propertyId': BOOKING_PROPERTY_ID,
            'bookingType': booking_type,
            'correlationId': 'tzg-schedule-check',
            'startDate': first.strftime( '%m/%d/%Y' ),
            'endDate': last.strftime( '%m/%d/%Y' ),
         },
      },
   )
   errors = payload.get( 'errors' )

   if errors:
      message = errors[ 0 ].get( 'message' ) if isinstance( errors[ 0 ], dict ) else errors[ 0 ]
      raise RuntimeError( str( message ) )

   data = payload.get( 'data' )

   if not isinstance( data, dict ):
      raise RuntimeError( 'Booking calendar response did not include data.' )

   year_rows = data.get( 'enabledDates' ) or []
   found: list[ date ] = []

   for year_row in year_rows:
      year = int( year_row[ 'year' ] )

      if year < 100:
         year += 2000

      for month_row in year_row[ 'months' ]:
         month = int( month_row[ 'month' ] )

         for day in month_row[ 'days' ]:
            found.append( date( year, month, int( day ) ) )

   return [
      scheduled_date
      for scheduled_date in found
      if first <= scheduled_date <= last
   ]


def format_date_list( dates: list[ date ] ) -> str:
   if not dates:
      return ''

   ordered = sorted( dates )
   ranges: list[ str ] = []
   start = ordered[ 0 ]
   previous = ordered[ 0 ]

   for current in ordered[ 1: ]:
      if current == previous + timedelta( days=1 ):
         previous = current
         continue

      ranges.append( format_date_span( start, previous ) )
      start = current
      previous = current

   ranges.append( format_date_span( start, previous ) )
   return ', '.join( ranges )


def format_date_span( start: date, end: date ) -> str:
   if start == end:
      return start.isoformat()

   return f'{ start.isoformat() } through { end.isoformat() }'


def names_only( names: set[ str ] ) -> list[ str ]:
   return [
      f'  { name }'
      for name in sorted( names, key=str.casefold )
   ]


def different_slot_lines(
      names: set[ str ],
      website_slots: dict[ str, set[ tuple[ int, str ] ] ],
      app_slots: dict[ str, set[ tuple[ int, str ] ] ] ) -> list[ str ]:
   lines = []

   for name in sorted( names, key=str.casefold ):
      lines.append(
         '\n'.join( [
            f'  { name }',
            f'    Website: { describe_slots( website_slots[ name ] ) }',
            f'    App: { describe_slots( app_slots[ name ] ) }',
         ] )
      )

   return lines


def window_lines(
      names: list[ str ],
      links: dict[ str, str ],
      schedules: list[ tuple[ str, date, date | None, str, set[ int ] ] ],
      first: date,
      last: date ) -> list[ str ]:
   lines = []

   for name in names:
      lines.append( window_line( name, links.get( name ), schedules, first, last ) )

   return lines


def window_line(
      name: str,
      link: str | None,
      schedules: list[ tuple[ str, date, date | None, str, set[ int ] ] ],
      first: date,
      last: date ) -> str:
   app_dates = scheduled_dates( schedules, name, first, last )
   detail = read_window_difference( link, app_dates, first, last )
   return f'  { name }\n{ detail }'


def read_window_difference(
      link: str | None,
      app_dates: list[ date ],
      first: date,
      last: date ) -> str:
   if link == None or link == '':
      return '    The app has no booking link for this encounter.'

   try:
      booking_type = booking_type_id( fetch_text( link ) )
   except RuntimeError as error:
      return f'    Could not read the booking page: { error }'

   if booking_type == None:
      return '    The booking page has no tour id.'

   try:
      bookable = booking_calendar_dates( booking_type, first, last )
   except ( RuntimeError, ValueError, KeyError, TypeError ) as error:
      return f'    Could not read the booking calendar: { error }'

   app_only = sorted( set( app_dates ) - set( bookable ) )
   bookable_only = sorted( set( bookable ) - set( app_dates ) )
   parts = []

   if app_only:
      parts.append( f'    App dates not bookable: { format_date_list( app_only ) }' )

   if bookable_only:
      parts.append( f'    Bookable dates not in the app: { format_date_list( bookable_only ) }' )

   if not parts:
      return ''

   return '\n'.join( parts )


def print_category( title: str, violations: list[ str ] ) -> None:
   print( f'{ title }: { len( violations ) }' )

   for violation in violations:
      if violation == '':
         continue

      print( violation )

   print()


def check_schedules( database: Path, today: date ) -> int:
   links, schedules = load_encounters( database )
   app_names_by_fold = {
      name.casefold(): name
      for name in links
   }
   website_slots = resolve_website_slots(
      parse_website_slots( fetch_text( WEBSITE_SCHEDULE_URL ) ),
      app_names_by_fold,
   )
   current_app_slots = active_slots( schedules, today )
   website_names = set( website_slots )
   app_names = set( current_app_slots )
   shared_names = website_names & app_names
   different_names = {
      name
      for name in shared_names
      if website_slots[ name ] != current_app_slots[ name ]
   }
   first = today + timedelta( days=1 )
   last = today + timedelta( days=BOOKING_HORIZON_DAYS )
   shared_name_list = sorted( shared_names, key=str.casefold )
   windows = [
      line
      for line in window_lines( shared_name_list, links, schedules, first, last )
      if line.split( '\n', 1 )[ 1 ] != ''
   ]
   only_in_app = names_only( app_names - website_names )
   only_on_website = names_only( website_names - app_names )
   different_slots = different_slot_lines(
      different_names,
      website_slots,
      current_app_slots,
   )

   print(
      f'Wild encounter schedule check for { today.isoformat() }. '
      f'Booking dates compared from { first.isoformat() } through { last.isoformat() }.'
   )
   print()
   print_category( 'Scheduled in the app and not on the website', only_in_app )
   print_category( 'Scheduled on the website and not in the app', only_on_website )
   print_category( 'Different days or times', different_slots )
   print_category( 'Windows which do not align', windows )

   return (
      len( only_in_app )
      + len( only_on_website )
      + len( different_slots )
      + len( windows )
   )


def main() -> int:
   args = parse_args()

   if not args.database.exists():
      print( f'Could not find { args.database }.', file=sys.stderr )
      return 2

   try:
      issues = check_schedules( args.database, date.today() )
   except RuntimeError as error:
      print( error, file=sys.stderr )
      return 2

   if issues:
      return 1

   return 0


if __name__ == '__main__':
   raise SystemExit( main() )
