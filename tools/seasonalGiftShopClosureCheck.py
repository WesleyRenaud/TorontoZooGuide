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
WEBSITE_GIFT_SHOPS_URL = 'https://www.torontozoo.com/tz/giftshops'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare gift shops closed for the season with the Toronto Zoo website '
         'while the seasonal curves are ramping down, and report app flags the '
         'website has cleared while the curves are ramping up.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def visible_page_html( page_html: str ) -> str:
   return re.sub( r'(?is)<!--.*?-->', '', page_html )


def parse_website_gift_shops( page_html: str, today: date ) -> list[ str ]:
   page_html = visible_page_html( page_html )
   openings = list( re.finditer( r'(?is)<(a|div) class="col3"[^>]*>', page_html ) )

   if not openings:
      raise RuntimeError( 'The gift shops page has no gift shop list.' )

   gift_shops = []

   for index, opening in enumerate( openings ):
      end = openings[ index + 1 ].start() if index + 1 < len( openings ) else len( page_html )
      body = page_html[ opening.end():end ]
      title_match = re.search( r'(?is)<strong>(.*?)</strong>', body )
      status_match = re.search( r'(?is)<span class="opentxt">(.*?)</span>', body )

      if status_match == None or title_match == None:
         continue

      if not is_closed_for_season_status( status_match.group( 1 ), today ):
         continue

      gift_shops.append( clean_html( title_match.group( 1 ) ) )

   return gift_shops


def load_status(
      database: Path,
      ) -> tuple[
         dict[ str, str ],
         set[ tuple[ str, bool, date | None, date | None, bool ] ],
         dict[ tuple[ str, str ], dict[ tuple[ int, int ], float ] ],
      ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      gift_shop_rows = connection.execute(
         """   SELECT
                  NAME
               FROM GiftShop
         """
      ).fetchall()
      status_rows = connection.execute(
         """   SELECT
                  GIFT_SHOP,
                  IS_CLOSED,
                  CLOSED_START,
                  CLOSED_END,
                  CLOSED_FOR_SEASON
               FROM GiftShopStatus
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
      for row in gift_shop_rows
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

   return catalog, statuses, curves


def app_closed_for_season_gift_shops(
      statuses: set[ tuple[ str, bool, date | None, date | None, bool ] ],
      today: date ) -> set[ str ]:
   return {
      gift_shop
      for gift_shop, is_closed, start, end, for_season in statuses
      if is_closed and for_season and covers_today( start, end, today )
   }


def matched_catalog_name( title: str, catalog: dict[ str, str ] ) -> str | None:
   return catalog.get( title.casefold() )


def print_category( title: str, gift_shops: list[ str ] ) -> None:
   print( f'{ title }: { len( gift_shops ) }' )

   for gift_shop in gift_shops:
      print( f'  { gift_shop }' )

   print()


def missed_website_gift_shops(
      listings: list[ str ],
      catalog: dict[ str, str ],
      app_gift_shops: set[ str ] ) -> list[ str ]:
   missed = []

   for title in listings:
      name = matched_catalog_name( title, catalog )

      if name == None or name in app_gift_shops or name in missed:
         continue

      missed.append( name )

   return sorted( missed, key=str.casefold )


def website_catalog_names( listings: list[ str ], catalog: dict[ str, str ] ) -> set[ str ]:
   names: set[ str ] = set()

   for title in listings:
      name = matched_catalog_name( title, catalog )

      if name != None:
         names.add( name )

   return names


def check_schedules( database: Path, today: date ) -> int:
   catalog, statuses, curves = load_status( database )

   if not curves:
      raise RuntimeError( 'The database has no seasonal viewability curves.' )

   ramping_down = is_ramping_down( curves, today )
   ramping_up = is_ramping_up( curves, today )

   if not ramping_down and not ramping_up:
      print(
         f'Seasonal gift shop closure check for { today.isoformat() }. '
         'The seasonal curves are not ramping down, so closed-for-season flags '
         'were not compared.'
      )
      return 0

   listings = parse_website_gift_shops( fetch_text( WEBSITE_GIFT_SHOPS_URL ), today )
   app_gift_shops = app_closed_for_season_gift_shops( statuses, today )
   extra = sorted(
      app_gift_shops - website_catalog_names( listings, catalog ),
      key=str.casefold,
   )

   if ramping_up:
      print( f'Seasonal gift shop closure check for { today.isoformat() }.' )
      print(
         'The seasonal curves are ramping up, so closed-for-season flags still set '
         'in the app were compared with the website.'
      )
      print()
      print_category( 'Closed for the season in the app and not on the website', extra )
      return len( extra )

   missed = missed_website_gift_shops( listings, catalog, app_gift_shops )

   print( f'Seasonal gift shop closure check for { today.isoformat() }.' )
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
