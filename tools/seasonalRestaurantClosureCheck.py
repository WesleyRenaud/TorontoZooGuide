from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import unquote

from tools.seasonalAttractionClosureCheck import is_closed_for_season_status
from tools.seasonalAttractionClosureCheck import normalize_path
from tools.seasonalOffDisplayCheck import clean_html
from tools.seasonalOffDisplayCheck import covers_today
from tools.seasonalOffDisplayCheck import fetch_text
from tools.seasonalOffDisplayCheck import is_ramping_down


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_RESTAURANTS_URL = 'https://www.torontozoo.com/tz/restaurants'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare restaurants closed for the season with the Toronto Zoo website '
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


def parse_website_restaurants( page_html: str, today: date ) -> list[ tuple[ str, str ] ]:
   openings = list( re.finditer( r'(?is)<(a|div) class="col3"[^>]*>', page_html ) )

   if not openings:
      raise RuntimeError( 'The restaurants page has no restaurant list.' )

   restaurants = []

   for index, opening in enumerate( openings ):
      end = openings[ index + 1 ].start() if index + 1 < len( openings ) else len( page_html )
      body = page_html[ opening.end():end ]
      href_match = re.search( r'href="([^"]*)"', opening.group( 0 ) )
      href = '' if href_match == None else href_match.group( 1 )
      status_match = re.search( r'(?is)<span class="opentxt">(.*?)</span>', body )
      title_match = re.search( r'(?is)<div class="col3title">(.*?)</div>', body )

      if status_match == None or title_match == None:
         continue

      if not is_closed_for_season_status( status_match.group( 1 ), today ):
         continue

      restaurants.append( ( href, clean_html( title_match.group( 1 ) ) ) )

   return restaurants


def load_status(
      database: Path,
      ) -> tuple[
         dict[ str, str ],
         dict[ str, str ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      restaurant_rows = connection.execute(
         """   SELECT
                  NAME,
                  MENU_LINK
               FROM Restaurant
         """
      ).fetchall()
      status_rows = connection.execute(
         """   SELECT
                  RESTAURANT,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               FROM RestaurantStatus
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
      for row in restaurant_rows
   }
   links = {
      str( row[ 0 ] ): str( row[ 1 ] )
      for row in restaurant_rows
      if row[ 1 ] != None and str( row[ 1 ] ).strip() != ''
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

   return catalog, links, statuses, curves


def app_closed_for_season_restaurants(
      statuses: set[ tuple[ str, bool, date | None, date | None, bool ] ],
      today: date ) -> set[ str ]:
   return {
      restaurant
      for restaurant, is_closed, start, end, for_season in statuses
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

   path = normalize_path( unquote( href ) )

   if path == '':
      return []

   return [
      name
      for name, link in links.items()
      if normalize_path( unquote( link ) ) == path
   ]


def print_category( title: str, restaurants: list[ str ] ) -> None:
   print( f'{ title }: { len( restaurants ) }' )

   for restaurant in restaurants:
      print( f'  { restaurant }' )

   print()


def missed_website_restaurants(
      listings: list[ tuple[ str, str ] ],
      catalog: dict[ str, str ],
      links: dict[ str, str ],
      app_restaurants: set[ str ] ) -> list[ str ]:
   missed = []

   for href, title in listings:
      for name in matched_catalog_names( title, href, catalog, links ):
         if name in app_restaurants or name in missed:
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
   catalog, links, statuses, curves = load_status( database )

   if not curves:
      raise RuntimeError( 'The database has no seasonal viewability curves.' )

   if not is_ramping_down( curves, today ):
      print(
         f'Seasonal restaurant closure check for { today.isoformat() }. '
         'The seasonal curves are not ramping down, so closed-for-season flags '
         'were not compared.'
      )
      return 0

   listings = parse_website_restaurants( fetch_text( WEBSITE_RESTAURANTS_URL ), today )
   app_restaurants = app_closed_for_season_restaurants( statuses, today )
   missed = missed_website_restaurants(
      listings,
      catalog,
      links,
      app_restaurants,
   )
   extra = sorted(
      app_restaurants - website_catalog_names( listings, catalog, links ),
      key=str.casefold,
   )

   print( f'Seasonal restaurant closure check for { today.isoformat() }.' )
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
