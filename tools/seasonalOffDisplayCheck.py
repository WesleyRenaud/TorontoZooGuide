from __future__ import annotations

import argparse
from datetime import date, timedelta
from html import unescape
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
from urllib.parse import unquote


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_ALERTS_URL = 'https://www.torontozoo.com/alerts'
USER_AGENT = 'Mozilla/5.0'
SEASON_STATUS = 'off for the season'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare animals off display for the season with the Toronto Zoo website '
         'while the seasonal curves are ramping down.'
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


def parse_website_animals( page_html: str ) -> list[ tuple[ str, str ] ]:
   if 'animals not currently viewable' not in page_html.casefold():
      raise RuntimeError( 'The alerts page has no off-display list.' )

   sections = re.split(
      r'(?is)<div class="atitle[^"]*" id="([^"]+)">',
      page_html,
   )

   if len( sections ) < 3:
      raise RuntimeError( 'The alerts page has no off-display sections.' )

   animals = []

   for index in range( 1, len( sections ), 2 ):
      section = unescape( unquote( sections[ index ] ) ).strip()

      for href, body in re.findall(
            r'(?is)<a href="/animals/([^"]+)"(.*?)</a>',
            sections[ index + 1 ] ):
         if 'status sseason' not in body.casefold():
            continue

         if SEASON_STATUS not in clean_html( body ).casefold():
            continue

         name = unescape( unquote( href ) ).replace( '+', ' ' ).strip()
         animals.append( ( section, name ) )

   return animals


def load_status(
      database: Path,
      ) -> tuple[
         dict[ str, str ],
         dict[ str, str ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      species_rows = connection.execute(
         """   SELECT SPECIES
               FROM Animal
         """
      ).fetchall()
      exhibit_rows = connection.execute(
         """   SELECT NAME
               FROM Exhibit
         """
      ).fetchall()
      exhibit_status_rows = connection.execute(
         """   SELECT
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               FROM ExhibitStatus
         """
      ).fetchall()
      status_rows = connection.execute(
         """   SELECT
                  SPECIES,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_FOR_SEASON
               FROM AnimalStatus
         """
      ).fetchall()
      curve_rows = connection.execute(
         """   SELECT
                  SPECIES,
                  EXHIBIT,
                  MONTH,
                  DAY,
                  VALUE
               FROM AnimalDaySeasonalViewabilityMultiplier
         """
      ).fetchall()
   finally:
      connection.close()

   catalog = {
      str( row[ 0 ] ).casefold(): str( row[ 0 ] )
      for row in species_rows
   }
   exhibits = {
      str( row[ 0 ] ).casefold(): str( row[ 0 ] )
      for row in exhibit_rows
   }
   exhibit_closures = {
      (
         str( row[ 0 ] ),
         bool( row[ 1 ] ),
         None if row[ 2 ] == None else date.fromisoformat( str( row[ 2 ] ) ),
         None if row[ 3 ] == None else date.fromisoformat( str( row[ 3 ] ) ),
         bool( row[ 4 ] ),
      )
      for row in exhibit_status_rows
   }
   statuses = {
      (
         str( row[ 0 ] ),
         bool( row[ 1 ] ),
         None if row[ 2 ] == None else date.fromisoformat( str( row[ 2 ] ) ),
         None if row[ 3 ] == None else date.fromisoformat( str( row[ 3 ] ) ),
         bool( row[ 4 ] ),
      )
      for row in status_rows
   }
   curves: dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ] = {}

   for species, exhibit, month, day, value in curve_rows:
      curve = curves.setdefault( ( str( species ), str( exhibit ) ), {} )
      curve[ ( int( month ), int( day ) ) ] = float( value )

   return catalog, exhibits, statuses, exhibit_closures, curves


def resolve_name( name: str, catalog: dict[ str, str ] ) -> str:
   return catalog.get( name.casefold(), name )


def covers_today(
      start: date | None,
      end: date | None,
      today: date ) -> bool:
   if start != None and today < start:
      return False

   if end != None and today > end:
      return False

   return True


def closed_for_season_exhibits(
      closures: set[ tuple[ str, bool, date | None, date | None, bool ] ],
      today: date ) -> set[ str ]:
   return {
      exhibit
      for exhibit, is_closed, start, end, for_season in closures
      if is_closed and for_season and covers_today( start, end, today )
   }


def app_off_season_animals(
      statuses: set[ tuple[ str, bool, date | None, date | None, bool ] ],
      today: date ) -> set[ str ]:
   return {
      species
      for species, is_off_display, start, end, for_season in statuses
      if is_off_display and for_season and covers_today( start, end, today )
   }


def is_ramping_down(
      curves: dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      today: date ) -> bool:
   yesterday = today - timedelta( days=1 )
   decreased = False
   increased = False

   for curve in curves.values():
      today_value = curve.get( ( today.month, today.day ) )
      yesterday_value = curve.get( ( yesterday.month, yesterday.day ) )

      if today_value == None or yesterday_value == None:
         continue

      if today_value < yesterday_value:
         decreased = True
      elif today_value > yesterday_value:
         increased = True

   return decreased and not increased


def print_category( title: str, animals: list[ str ] ) -> None:
   print( f'{ title }: { len( animals ) }' )

   for animal in animals:
      print( f'  { animal }' )

   print()


def missed_website_animals(
      listings: list[ tuple[ str, str ] ],
      catalog: dict[ str, str ],
      exhibits: dict[ str, str ],
      app_animals: set[ str ],
      closed_exhibits: set[ str ] ) -> list[ str ]:
   missed = []

   for section, raw_name in listings:
      species = resolve_name( raw_name, catalog )
      exhibit = exhibits.get( section.casefold() )
      covered_by_exhibit = exhibit != None and exhibit in closed_exhibits

      if species in app_animals or covered_by_exhibit or species in missed:
         continue

      missed.append( species )

   return sorted( missed, key=str.casefold )


def check_schedules( database: Path, today: date ) -> int:
   catalog, exhibits, statuses, exhibit_closures, curves = load_status( database )

   if not curves:
      raise RuntimeError( 'The database has no seasonal viewability curves.' )

   if not is_ramping_down( curves, today ):
      print(
         f'Seasonal off-display check for { today.isoformat() }. '
         'The seasonal curves are not ramping down, so off-display flags were not compared.'
      )
      return 0

   listings = parse_website_animals( fetch_text( WEBSITE_ALERTS_URL ) )
   website_animals = {
      resolve_name( name, catalog )
      for _section, name in listings
   }
   app_animals = app_off_season_animals( statuses, today )
   closed_exhibits = closed_for_season_exhibits( exhibit_closures, today )
   missed = missed_website_animals(
      listings,
      catalog,
      exhibits,
      app_animals,
      closed_exhibits,
   )
   extra = sorted( app_animals - website_animals, key=str.casefold )

   print( f'Seasonal off-display check for { today.isoformat() }.' )
   print()
   print_category( 'Off for the season on the website and not in the app', missed )
   print_category( 'Off for the season in the app and not on the website', extra )

   return len( missed ) + len( extra )


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
