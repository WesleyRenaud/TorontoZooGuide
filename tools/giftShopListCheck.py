from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sqlite3
import sys

from tools.seasonalGiftShopClosureCheck import visible_page_html
from tools.seasonalOffDisplayCheck import clean_html
from tools.seasonalOffDisplayCheck import fetch_text


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_GIFT_SHOPS_URL = 'https://www.torontozoo.com/tz/giftshops'
DASHES = '-\u2010\u2011\u2012\u2013\u2014'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare gift shops listed on the Toronto Zoo website with the gift '
         'shops in the app.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def normalize_name( name: str ) -> str:
   text = (
      name
      .replace( '\u2018', "'" )
      .replace( '\u2019', "'" )
      .replace( '\u201b', "'" )
   )
   text = re.sub( r'\s*\([^)]*\)', '', text )
   text = re.sub( f'[{ DASHES }]', ' ', text )
   text = text.casefold()
   return re.sub( r'\s+', ' ', text ).strip()


def parse_website_gift_shops( page_html: str ) -> list[ str ]:
   page_html = visible_page_html( page_html )
   openings = list( re.finditer( r'(?is)<(a|div) class="col3"[^>]*>', page_html ) )

   if not openings:
      raise RuntimeError( 'The gift shops page has no gift shop list.' )

   gift_shops = []

   for index, opening in enumerate( openings ):
      end = openings[ index + 1 ].start() if index + 1 < len( openings ) else len( page_html )
      body = page_html[ opening.end():end ]
      title_match = re.search( r'(?is)<strong>(.*?)</strong>', body )

      if title_match == None:
         raise RuntimeError( 'A gift shop listing has no title.' )

      title = clean_html( title_match.group( 1 ) )

      if title == '' or title in gift_shops:
         continue

      gift_shops.append( title )

   if not gift_shops:
      raise RuntimeError( 'The gift shops page has no gift shop list.' )

   return gift_shops


def fetch_website_gift_shops() -> list[ str ]:
   return parse_website_gift_shops( fetch_text( WEBSITE_GIFT_SHOPS_URL ) )


def load_gift_shops( database: Path ) -> dict[ str, list[ str ] ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      rows = connection.execute(
         """   SELECT NAME
               FROM GiftShop
               ORDER BY NAME
         """
      ).fetchall()
   finally:
      connection.close()

   names_by_key: dict[ str, list[ str ] ] = {}

   for row in rows:
      official = str( row[ 0 ] )
      names_by_key.setdefault( normalize_name( official ), [] ).append( official )

   return names_by_key


def add_listing( listings: dict[ str, list[ str ] ], name: str ) -> None:
   names = listings.setdefault( normalize_name( name ), [] )

   if name not in names:
      names.append( name )


def listing_label( names: list[ str ] ) -> str:
   return ' / '.join( sorted( names, key=str.casefold ) )


def missing_labels(
      source: dict[ str, list[ str ] ],
      other: dict[ str, list[ str ] ] ) -> list[ str ]:
   labels = []

   for key, names in source.items():
      if key in other:
         continue

      labels.append( listing_label( names ) )

   return sorted( labels, key=str.casefold )


def print_category( title: str, gift_shops: list[ str ] ) -> None:
   print( f'{ title }: { len( gift_shops ) }' )

   for gift_shop in gift_shops:
      print( f'  { gift_shop }' )

   print()


def check_lists( database: Path, today: date ) -> int:
   names_by_key = load_gift_shops( database )
   app_listings: dict[ str, list[ str ] ] = {}
   website_listings: dict[ str, list[ str ] ] = {}

   for names in names_by_key.values():
      for name in names:
         add_listing( app_listings, name )

   for title in fetch_website_gift_shops():
      matches = names_by_key.get( normalize_name( title ) )

      if matches != None:
         for name in matches:
            add_listing( website_listings, name )

         continue

      add_listing( website_listings, title )

   website_only = missing_labels( website_listings, app_listings )
   app_only = missing_labels( app_listings, website_listings )

   print( f'Gift shop list check for { today.isoformat() }.' )
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
