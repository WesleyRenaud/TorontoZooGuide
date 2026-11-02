from __future__ import annotations

import argparse
import calendar
from datetime import date
from pathlib import Path
import re
import sqlite3
import sys

from tools.seasonalOffDisplayCheck import clean_html
from tools.seasonalOffDisplayCheck import closed_for_season_exhibits
from tools.seasonalOffDisplayCheck import covers_today
from tools.seasonalOffDisplayCheck import fetch_text
from tools.seasonalOffDisplayCheck import is_ramping_down
from tools.seasonalOffDisplayCheck import resolve_name


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_ATTRACTIONS_URL = 'https://www.torontozoo.com/attractions'
SEASON_STATUS = 'closed for the season'
THROUGH_DATE_RE = re.compile(
   r'through\s+([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?(?:\s*,?\s*(\d{4}))?'
)


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare attractions closed for the season with the Toronto Zoo website '
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


def normalize_path( url: str ) -> str:
   trimmed = url.split( '?', 1 )[ 0 ].strip()

   if '://' in trimmed:
      trimmed = trimmed.split( '://', 1 )[ 1 ]
      trimmed = trimmed.split( '/', 1 )[ 1 ] if '/' in trimmed else ''

   return trimmed.strip( '/' ).casefold()


def month_number( name: str ) -> int | None:
   for number, month in enumerate( calendar.month_name ):
      if month.casefold() == name:
         return number

   return None


def through_date( status: str, today: date ) -> date | None:
   match = THROUGH_DATE_RE.search( status.casefold() )

   if match == None:
      return None

   month = month_number( match.group( 1 ) )

   if month == None:
      return None

   year = today.year if match.group( 3 ) == None else int( match.group( 3 ) )

   try:
      return date( year, month, int( match.group( 2 ) ) )
   except ValueError:
      return None


def is_closed_for_season_status( status: str, today: date ) -> bool:
   cleaned = clean_html( status ).casefold()

   if SEASON_STATUS in cleaned:
      return True

   ended = through_date( cleaned, today )
   return ended != None and ended < today


def parse_website_attractions( page_html: str, today: date ) -> list[ tuple[ str, str ] ]:
   cards = re.findall(
      r'(?is)<a class="col3"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
      page_html,
   )

   if not cards:
      raise RuntimeError( 'The attractions page has no attraction list.' )

   attractions = []

   for href, body in cards:
      status_match = re.search( r'(?is)<span class="opentxt">(.*?)</span>', body )
      title_match = re.search( r'(?is)<div class="col3title">(.*?)</div>', body )

      if status_match == None or title_match == None:
         continue

      if not is_closed_for_season_status( status_match.group( 1 ), today ):
         continue

      attractions.append( ( href, clean_html( title_match.group( 1 ) ) ) )

   return attractions


def load_status(
      database: Path,
      ) -> tuple[
         dict[ str, str ],
         dict[ str, str ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         dict[ str, str ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      attraction_rows = connection.execute(
         """   SELECT
                  NAME,
                  INFO_LINK
               FROM Attraction
         """
      ).fetchall()
      status_rows = connection.execute(
         """   SELECT
                  ATTRACTION,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               FROM AttractionStatus
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
      for row in attraction_rows
   }
   links = {
      str( row[ 0 ] ): str( row[ 1 ] )
      for row in attraction_rows
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
   curves: dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ] = {}

   for species, exhibit, month, day, value in curve_rows:
      curve = curves.setdefault( ( str( species ), str( exhibit ) ), {} )
      curve[ ( int( month ), int( day ) ) ] = float( value )

   return catalog, links, statuses, exhibits, exhibit_closures, curves


def app_closed_for_season_attractions(
      statuses: set[ tuple[ str, bool, date | None, date | None, bool ] ],
      today: date ) -> set[ str ]:
   return {
      attraction
      for attraction, is_closed, start, end, for_season in statuses
      if is_closed and for_season and covers_today( start, end, today )
   }


def matched_catalog_names(
      title: str,
      href: str,
      catalog: dict[ str, str ],
      links: dict[ str, str ] ) -> list[ str ]:
   named = catalog.get( title.casefold() )

   if named != None:
      return [ named ]

   path = normalize_path( href )

   if path == '':
      return []

   return [
      name
      for name, link in links.items()
      if normalize_path( link ) == path
   ]


def print_category( title: str, attractions: list[ str ] ) -> None:
   print( f'{ title }: { len( attractions ) }' )

   for attraction in attractions:
      print( f'  { attraction }' )

   print()


def missed_website_attractions(
      listings: list[ tuple[ str, str ] ],
      catalog: dict[ str, str ],
      links: dict[ str, str ],
      exhibits: dict[ str, str ],
      app_attractions: set[ str ],
      closed_exhibits: set[ str ] ) -> list[ str ]:
   missed = []

   for href, title in listings:
      matches = matched_catalog_names( title, href, catalog, links )

      if not matches:
         name = resolve_name( title, exhibits )

         if name in closed_exhibits or name in missed:
            continue

         missed.append( name )

         continue

      for name in matches:
         if name in app_attractions or name in missed:
            continue

         missed.append( name )

   return sorted( missed, key=str.casefold )


def website_catalog_names(
      listings: list[ tuple[ str, str ] ],
      catalog: dict[ str, str ],
      links: dict[ str, str ] ) -> set[ str ]:
   names: set[ str ] = set()

   for href, title in listings:
      names.update( matched_catalog_names( title, href, catalog, links ) )

   return names


def check_schedules( database: Path, today: date ) -> int:
   catalog, links, statuses, exhibits, exhibit_closures, curves = load_status( database )

   if not curves:
      raise RuntimeError( 'The database has no seasonal viewability curves.' )

   if not is_ramping_down( curves, today ):
      print(
         f'Seasonal attraction closure check for { today.isoformat() }. '
         'The seasonal curves are not ramping down, so closed-for-season flags '
         'were not compared.'
      )
      return 0

   listings = parse_website_attractions( fetch_text( WEBSITE_ATTRACTIONS_URL ), today )
   app_attractions = app_closed_for_season_attractions( statuses, today )
   closed_exhibits = closed_for_season_exhibits( exhibit_closures, today )
   missed = missed_website_attractions(
      listings,
      catalog,
      links,
      exhibits,
      app_attractions,
      closed_exhibits,
   )
   extra = sorted(
      app_attractions - website_catalog_names( listings, catalog, links ),
      key=str.casefold,
   )

   print( f'Seasonal attraction closure check for { today.isoformat() }.' )
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
