from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path
import re
import sqlite3
import subprocess
import sys


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_SCHEDULE_URL = 'https://www.torontozoo.com/MeetTheGuardians'
USER_AGENT = 'Mozilla/5.0'
WEEKDAY_LABELS = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
DISPLAY_WEEKDAYS = [ 6, 0, 1, 2, 3, 4, 5 ]
MONTHS = {
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
NAME_ALIASES = {
   'blue and yellow macaw': 'Blue And Yellow Macaw',
}
LOCATION_ALIASES = {
   'african rainforest': [ 'African Rainforest Pavilion' ],
   'african savanna': [ 'Africa Savanna' ],
   'americas': [
      'Americas Pavilion',
      'Americas Outdoor Mayan Temple Ruins',
   ],
   'australasia': [
      'Australasia Outdoor',
      'Australasia Pavilion',
   ],
   'canadian domain': [ 'Canadian Domain' ],
   'eurasia': [ 'Eurasia Wilds' ],
   'indo-malaya': [
      'Indo-Malaya Outdoor',
      'Indo-Malaya Pavilion',
   ],
   'indo-malaya outdoor': [ 'Indo-Malaya Outdoor' ],
   'tundra trek': [ 'Tundra Trek' ],
}


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare guardians talks with the dates listed on the Toronto Zoo website.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def fetch_text( url: str ) -> str:
   result = subprocess.run(
      [ 'curl', '-fsS', '--max-time', '30', '-A', USER_AGENT, url ],
      check=False,
      capture_output=True,
   )

   if result.returncode != 0:
      detail = result.stderr.decode( errors='replace' ).strip()
      raise RuntimeError( detail or f'curl exited { result.returncode }' )

   return result.stdout.decode()


def clean_html( value: str ) -> str:
   text = re.sub( r'(?is)<[^>]+>', ' ', value )
   return re.sub( r'\s+', ' ', unescape( text ) ).strip()


def format_clock( parsed: datetime ) -> str:
   hour = parsed.hour % 12 or 12
   minute = str( parsed.minute ).zfill( 2 )
   suffix = 'AM' if parsed.hour < 12 else 'PM'
   return f'{ hour }:{ minute } { suffix }'


def normalize_clock( value: str ) -> str:
   text = re.sub( r'\s+', '', value ).upper()

   try:
      return format_clock( datetime.strptime( text, '%I:%M%p' ) )
   except ValueError:
      return value.strip()


def format_days( weekdays: set[ int ] ) -> str:
   return ', '.join(
      WEEKDAY_LABELS[ weekday ]
      for weekday in DISPLAY_WEEKDAYS
      if weekday in weekdays
   )


def describe_slots( slots: set[ tuple[ int, str ] ] ) -> str:
   by_time: dict[ str, set[ int ] ] = {}

   for weekday, talk_time in slots:
      by_time.setdefault( talk_time, set() ).add( weekday )

   descriptions = []

   for talk_time in sorted( by_time ):
      descriptions.append( f'{ talk_time } { format_days( by_time[ talk_time ] ) }' )

   return '; '.join( descriptions )


def parse_heading( heading: str, today: date ) -> date | None:
   words = heading.replace( ',', '' ).split()

   if len( words ) < 2 or words[ -2 ].casefold() not in MONTHS:
      return None

   month = MONTHS[ words[ -2 ].casefold() ]
   day = int( words[ -1 ] )
   scheduled_date = date( today.year, month, day )

   if scheduled_date < today - timedelta( days=1 ):
      return date( today.year + 1, month, day )

   if scheduled_date > today + timedelta( days=45 ):
      return date( today.year - 1, month, day )

   return scheduled_date


def parse_programme(
      page_html: str,
      today: date ) -> tuple[ list[ date ], list[ tuple[ date, str, str, str ] ] ]:
   marker = '<div class="programme-schedule">'
   start = page_html.find( marker )

   if start < 0:
      raise RuntimeError( 'The guardians page has no programme schedule.' )

   sections = re.split(
      r'(?is)<div class="cstrong">',
      page_html[ start: ],
   )

   if len( sections ) < 2:
      raise RuntimeError( 'The guardians page has no schedule dates.' )

   dates: list[ date ] = []
   talks: list[ tuple[ date, str, str, str ] ] = []

   for section in sections[ 1: ]:
      heading, _, rest = section.partition( '</div>' )
      scheduled_date = parse_heading( clean_html( heading ), today )

      if scheduled_date == None:
         break

      dates.append( scheduled_date )
      names = [
         clean_html( name )
         for name in re.findall( r'(?is)<div class="aname">(.*?)</div>', rest )
      ]
      locations = [
         clean_html( location )
         for location in re.findall(
            r'(?is)<div class="talklocation">(.*?)</div>',
            rest,
         )
      ]
      times = [
         normalize_clock( talk_time )
         for talk_time in re.findall( r'(?i)(\d{1,2}:\d{2}\s*[ap]m)', rest )
      ]

      if not len( names ) == len( locations ) == len( times ):
         raise RuntimeError(
            f'The guardians schedule for { scheduled_date.isoformat() } '
            'could not be read.'
         )

      for name, location, talk_time in zip( names, locations, times ):
         talks.append( ( scheduled_date, talk_time, name, location ) )

   if not dates:
      raise RuntimeError( 'The guardians page has no schedule dates.' )

   return dates, talks


def stored_text( value: str | None ) -> str:
   if value == None:
      return ''

   return str( value )


def load_talks(
      database: Path,
      ) -> tuple[
         list[ tuple[ str, str ] ],
         set[ tuple[ str, str, str ] ],
         list[ tuple[ str, str, str, date, date | None, str, set[ int ] ] ],
         set[ tuple[ str, str, str, str, str ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      catalog_rows = connection.execute(
         """   SELECT
                  NAME,
                  LOCATION,
                  ENCLOSURE_NAME
               FROM MeetTheGuardiansTalk
         """
      ).fetchall()
      schedule_rows = connection.execute(
         """   SELECT
                  TALK_NAME,
                  LOCATION,
                  ENCLOSURE_NAME,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  TALK_TIME
               FROM GuardiansTalkSchedule
         """
      ).fetchall()
      cancellation_rows = connection.execute(
         """   SELECT
                  TALK_NAME,
                  LOCATION,
                  ENCLOSURE_NAME,
                  CANCELLATION_DATE,
                  TALK_TIME
               FROM GuardiansTalkCancellation
         """
      ).fetchall()
   finally:
      connection.close()

   catalog: list[ tuple[ str, str ] ] = []
   talk_keys: set[ tuple[ str, str, str ] ] = set()

   for name, location, enclosure in catalog_rows:
      identity = ( str( name ), str( location ) )
      talk_keys.add( ( identity[ 0 ], identity[ 1 ], stored_text( enclosure ) ) )

      if identity not in catalog:
         catalog.append( identity )
   schedules = []

   for row in schedule_rows:
      end = None if row[ 4 ] == None else date.fromisoformat( str( row[ 4 ] ) )
      weekdays = {
         index
         for index, flag in enumerate( row[ 5:12 ] )
         if flag
      }
      schedules.append( (
         str( row[ 0 ] ),
         str( row[ 1 ] ),
         stored_text( row[ 2 ] ),
         date.fromisoformat( str( row[ 3 ] ) ),
         end,
         normalize_clock( str( row[ 12 ] ) ),
         weekdays,
      ) )

   cancellations = {
      (
         str( row[ 0 ] ),
         str( row[ 1 ] ),
         stored_text( row[ 2 ] ),
         str( row[ 3 ] ),
         normalize_clock( str( row[ 4 ] ) ),
      )
      for row in cancellation_rows
   }
   return catalog, talk_keys, schedules, cancellations


def resolve_talk(
      name: str,
      location: str,
      catalog: list[ tuple[ str, str ] ] ) -> tuple[ str, str ]:
   canonical_name = NAME_ALIASES.get( name.casefold(), name )
   candidates = [
      row
      for row in catalog
      if row[ 0 ].casefold() == canonical_name.casefold()
   ]
   choices = LOCATION_ALIASES.get( location.casefold() )

   if choices != None:
      located = [
         row
         for row in candidates
         if row[ 1 ] in choices
      ]
   else:
      located = [
         row
         for row in candidates
         if row[ 1 ].casefold() == location.casefold()
      ]

   if located:
      return located[ 0 ][ 0 ], located[ 0 ][ 1 ]

   return name, location


def website_occurrences(
      talks: list[ tuple[ date, str, str, str ] ],
      catalog: list[ tuple[ str, str ] ],
      ) -> dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ]:
   occurrences: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ] = {}

   for scheduled_date, talk_time, name, location in talks:
      identity = resolve_talk( name, location, catalog )
      occurrences.setdefault( identity, set() ).add( ( scheduled_date, talk_time ) )

   return occurrences


def app_occurrences(
      schedules: list[ tuple[ str, str, str, date, date | None, str, set[ int ] ] ],
      cancellations: set[ tuple[ str, str, str, str, str ] ],
      window: set[ date ],
      talk_keys: set[ tuple[ str, str, str ] ],
      ) -> dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ]:
   occurrences: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ] = {}

   for scheduled_date in sorted( window ):
      weekday = scheduled_date.weekday()

      for name, location, enclosure, start, end, talk_time, weekdays in schedules:
         covers = start <= scheduled_date and ( end == None or end > scheduled_date )
         cancelled = (
            name,
            location,
            enclosure,
            scheduled_date.isoformat(),
            talk_time,
         ) in cancellations

         if ( name, location, enclosure ) not in talk_keys:
            continue

         if not covers or weekday not in weekdays or cancelled:
            continue

         identity = ( name, location )
         occurrences.setdefault( identity, set() ).add( ( scheduled_date, talk_time ) )

   return occurrences


def label( identity: tuple[ str, str ] ) -> str:
   return f'{ identity[ 0 ] }, { identity[ 1 ] }'


def names_only( identities: set[ tuple[ str, str ] ] ) -> list[ str ]:
   return [
      f'  { label( identity ) }'
      for identity in sorted( identities, key=label )
   ]


def slot_pairs(
      occurrences: set[ tuple[ date, str ] ] ) -> set[ tuple[ int, str ] ]:
   return {
      ( scheduled_date.weekday(), talk_time )
      for scheduled_date, talk_time in occurrences
   }


def different_slot_lines(
      identities: set[ tuple[ str, str ] ],
      website: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ],
      app: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ] ) -> list[ str ]:
   lines = []

   for identity in sorted( identities, key=label ):
      lines.append(
         '\n'.join( [
            f'  { label( identity ) }',
            f'    Website: { describe_slots( slot_pairs( website[ identity ] ) ) }',
            f'    App: { describe_slots( slot_pairs( app[ identity ] ) ) }',
         ] )
      )

   return lines


def format_date_span( start: date, end: date ) -> str:
   if start == end:
      return start.isoformat()

   return f'{ start.isoformat() } through { end.isoformat() }'


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


def window_lines(
      identities: set[ tuple[ str, str ] ],
      website: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ],
      app: dict[ tuple[ str, str ], set[ tuple[ date, str ] ] ] ) -> list[ str ]:
   lines = []

   for identity in sorted( identities, key=label ):
      website_dates = { item[ 0 ] for item in website[ identity ] }
      app_dates = { item[ 0 ] for item in app[ identity ] }
      parts = [ f'  { label( identity ) }' ]
      app_only = sorted( app_dates - website_dates )
      website_only = sorted( website_dates - app_dates )

      if app_only:
         parts.append( f'    App dates not on the website: { format_date_list( app_only ) }' )

      if website_only:
         parts.append(
            f'    Website dates not in the app: { format_date_list( website_only ) }'
         )

      if len( parts ) > 1:
         lines.append( '\n'.join( parts ) )

   return lines


def print_category( title: str, violations: list[ str ] ) -> None:
   print( f'{ title }: { len( violations ) }' )

   for violation in violations:
      if violation == '':
         continue

      print( violation )

   print()


def check_schedules( database: Path, today: date ) -> int:
   catalog, talk_keys, schedules, cancellations = load_talks( database )
   window_dates, talks = parse_programme( fetch_text( WEBSITE_SCHEDULE_URL ), today )
   compared_dates = [
      scheduled_date
      for scheduled_date in window_dates
      if scheduled_date > today
   ]
   upcoming_talks = [
      talk
      for talk in talks
      if talk[ 0 ] > today
   ]
   website = website_occurrences( upcoming_talks, catalog )
   app = app_occurrences(
      schedules,
      cancellations,
      set( compared_dates ),
      talk_keys,
   )
   website_names = set( website )
   app_names = set( app )
   shared_names = website_names & app_names
   different_names = {
      identity
      for identity in shared_names
      if slot_pairs( website[ identity ] ) != slot_pairs( app[ identity ] )
   }
   only_in_app = names_only( app_names - website_names )
   only_on_website = names_only( website_names - app_names )
   different_slots = different_slot_lines( different_names, website, app )
   windows = window_lines( shared_names, website, app )

   if compared_dates:
      first = min( compared_dates )
      last = max( compared_dates )
      span = (
         f'Website dates compared from { first.isoformat() } '
         f'through { last.isoformat() }.'
      )
   else:
      span = f'No website dates after { today.isoformat() }.'

   print( f'Guardians talk schedule check for { today.isoformat() }. { span }' )
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
