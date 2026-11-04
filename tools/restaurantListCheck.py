from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import unquote

from tools.seasonalAttractionClosureCheck import normalize_path
from tools.seasonalOffDisplayCheck import clean_html
from tools.seasonalOffDisplayCheck import fetch_text


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_RESTAURANTS_URL = 'https://www.torontozoo.com/tz/restaurants'
DASHES = '-\u2010\u2011\u2012\u2013\u2014'
ALLOWED_WEBSITE_ONLY_RESTAURANTS = {
   'Ice Cream Carts',
}


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare restaurants listed on the Toronto Zoo website with the '
         'restaurants in the app.'
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


def parse_website_restaurants( page_html: str ) -> list[ tuple[ str, str ] ]:
   openings = list( re.finditer( r'(?is)<(a|div) class="col3"[^>]*>', page_html ) )

   if not openings:
      raise RuntimeError( 'The restaurants page has no restaurant list.' )

   restaurants = []

   for index, opening in enumerate( openings ):
      end = openings[ index + 1 ].start() if index + 1 < len( openings ) else len( page_html )
      body = page_html[ opening.end():end ]
      href_match = re.search( r'href="([^"]*)"', opening.group( 0 ) )
      href = '' if href_match == None else href_match.group( 1 )
      title_match = re.search( r'(?is)<div class="col3title">(.*?)</div>', body )

      if title_match == None:
         raise RuntimeError( 'A restaurant listing has no title.' )

      title = clean_html( title_match.group( 1 ) )
      listing = ( href, title )

      if title == '' or listing in restaurants:
         continue

      restaurants.append( listing )

   if not restaurants:
      raise RuntimeError( 'The restaurants page has no restaurant list.' )

   return restaurants


def fetch_website_restaurants() -> list[ tuple[ str, str ] ]:
   return parse_website_restaurants( fetch_text( WEBSITE_RESTAURANTS_URL ) )


def load_restaurants( database: Path ) -> tuple[ dict[ str, list[ str ] ], dict[ str, str ] ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      rows = connection.execute(
         """   SELECT
                  NAME,
                  MENU_LINK
               FROM Restaurant
               ORDER BY NAME
         """
      ).fetchall()
   finally:
      connection.close()

   names_by_key: dict[ str, list[ str ] ] = {}
   links: dict[ str, str ] = {}

   for name, link in rows:
      official = str( name )

      if link != None and str( link ).strip() != '':
         links[ official ] = str( link )

      names_by_key.setdefault( normalize_name( official ), [] ).append( official )

   return names_by_key, links


def matched_catalog_names(
      title: str,
      href: str,
      names_by_key: dict[ str, list[ str ] ],
      links: dict[ str, str ] ) -> list[ str ]:
   named = names_by_key.get( normalize_name( title ) )

   if named != None:
      return named

   path = normalize_path( unquote( href ) )

   if path == '':
      return []

   return sorted(
      [
         name
         for name, link in links.items()
         if normalize_path( unquote( link ) ) == path
      ],
      key=str.casefold,
   )


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


def print_category( title: str, restaurants: list[ str ] ) -> None:
   print( f'{ title }: { len( restaurants ) }' )

   for restaurant in restaurants:
      print( f'  { restaurant }' )

   print()


def check_lists( database: Path, today: date ) -> int:
   names_by_key, links = load_restaurants( database )
   app_listings: dict[ str, list[ str ] ] = {}
   website_listings: dict[ str, list[ str ] ] = {}

   for names in names_by_key.values():
      for name in names:
         add_listing( app_listings, name )

   for href, title in fetch_website_restaurants():
      matches = matched_catalog_names( title, href, names_by_key, links )

      if matches:
         for name in matches:
            add_listing( website_listings, name )

         continue

      add_listing( website_listings, title )

   allowed_keys = {
      normalize_name( name )
      for name in ALLOWED_WEBSITE_ONLY_RESTAURANTS
   }
   unapproved_website_listings = {
      key: names
      for key, names in website_listings.items()
      if key not in allowed_keys
   }
   website_only = missing_labels( unapproved_website_listings, app_listings )
   app_only = missing_labels( app_listings, website_listings )

   print( f'Restaurant list check for { today.isoformat() }.' )
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
