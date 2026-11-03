from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sqlite3
import sys

from tools.seasonalAttractionClosureCheck import is_closed_for_season_status
from tools.seasonalOffDisplayCheck import clean_html
from tools.seasonalOffDisplayCheck import covers_today
from tools.seasonalOffDisplayCheck import fetch_text
from tools.seasonalOffDisplayCheck import is_ramping_down
from tools.seasonalOffDisplayCheck import is_ramping_up


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_ALERTS_URL = 'https://www.torontozoo.com/alerts'
FOUNTAIN_NAME = 'Drinking fountains'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare drinking fountains closed for the season with the Toronto Zoo '
         'alerts page while the seasonal curves are ramping down, and report an '
         'app flag the website has cleared while the curves are ramping up.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def notice_bodies( page_html: str ) -> list[ str ]:
   section_match = re.search(
      r'(?is)<h2[^>]*id="notices"[^>]*>.*?</h2>(.*?)(?:<h2[^>]*id="animals|\Z)',
      page_html,
   )

   if section_match == None:
      raise RuntimeError( 'The alerts page has no notices.' )

   section = section_match.group( 1 )
   openings = list( re.finditer( r'(?is)<div class="box[^"]*"[^>]*>', section ) )

   if openings:
      bodies = []

      for index, opening in enumerate( openings ):
         end = openings[ index + 1 ].start() if index + 1 < len( openings ) else len( section )
         bodies.append( section[ opening.end():end ] )

      return bodies

   return re.findall( r'(?is)<span>\s*<p>(.*?)</p>', section )


def fountains_closed_on_website( page_html: str, today: date ) -> bool:
   bodies = notice_bodies( page_html )

   if not bodies:
      raise RuntimeError( 'The alerts page has no notices.' )

   for body in bodies:
      text = clean_html( body )

      if 'fountain' not in text.casefold():
         continue

      if is_closed_for_season_status( text, today ):
         return True

   return False


def load_status(
      database: Path,
      ) -> tuple[
         tuple[ bool, date | None, date | None ] | None,
         dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      status_row = connection.execute(
         """   SELECT
                  IS_CLOSED,
                  START_DATE,
                  END_DATE
               FROM DrinkingFountainStatus
               LIMIT 1
         """
      ).fetchone()
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

   status = None

   if status_row != None:
      status = (
         bool( status_row[ 0 ] ),
         None if status_row[ 1 ] == None else date.fromisoformat( str( status_row[ 1 ] ) ),
         None if status_row[ 2 ] == None else date.fromisoformat( str( status_row[ 2 ] ) ),
      )

   curves: dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ] = {}

   for species, exhibit, month, day, value in curve_rows:
      curve = curves.setdefault( ( str( species ), str( exhibit ) ), {} )
      curve[ ( int( month ), int( day ) ) ] = float( value )

   return status, curves


def app_fountains_closed(
      status: tuple[ bool, date | None, date | None ] | None,
      today: date ) -> bool:
   if status == None:
      return False

   is_closed, start, end = status
   return is_closed and covers_today( start, end, today )


def print_category( title: str, names: list[ str ] ) -> None:
   print( f'{ title }: { len( names ) }' )

   for name in names:
      print( f'  { name }' )

   print()


def check_schedules( database: Path, today: date ) -> int:
   status, curves = load_status( database )

   if not curves:
      raise RuntimeError( 'The database has no seasonal viewability curves.' )

   ramping_down = is_ramping_down( curves, today )
   ramping_up = is_ramping_up( curves, today )

   if not ramping_down and not ramping_up:
      print(
         f'Seasonal drinking fountain closure check for { today.isoformat() }. '
         'The seasonal curves are not ramping down, so closed-for-season flags '
         'were not compared.'
      )
      return 0

   website_closed = fountains_closed_on_website( fetch_text( WEBSITE_ALERTS_URL ), today )
   app_closed = app_fountains_closed( status, today )
   extra = [ FOUNTAIN_NAME ] if app_closed and not website_closed else []

   if ramping_up:
      print( f'Seasonal drinking fountain closure check for { today.isoformat() }.' )
      print(
         'The seasonal curves are ramping up, so closed-for-season flags still set '
         'in the app were compared with the website.'
      )
      print()
      print_category( 'Closed for the season in the app and not on the website', extra )
      return len( extra )

   missed = [ FOUNTAIN_NAME ] if website_closed and not app_closed else []

   print( f'Seasonal drinking fountain closure check for { today.isoformat() }.' )
   print()
   print_category( 'Closed for the season on the website and not in the app', missed )
   print_category( 'Closed for the season in the app and not on the website', extra )

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
