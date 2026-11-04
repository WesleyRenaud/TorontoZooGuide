from __future__ import annotations

import argparse
from datetime import date
from html import unescape
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import unquote

from tools.seasonalOffDisplayCheck import fetch_text


ROOT = Path( __file__ ).resolve().parents[ 1 ]
WEBSITE_ANIMALS_URL = 'https://www.torontozoo.com/animals'
WEBSITE_REGION_PATHS = (
   'africa',
   'americas',
   'australasia',
   'canada',
   'discovery',
   'eurasia',
   'indo-malaya',
   'tundra',
)
DASHES = '-\u2010\u2011\u2012\u2013\u2014'
WEBSITE_NAME_ALIASES = {
   'wood bison female herd': 'wood bison',
   'wood bison male herd': 'wood bison',
}
ALLOWED_APP_ONLY_ANIMALS = {
   ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ( 'Great Horned Owl', 'Americas Pavilion' ),
   ( 'Greater Kudu', 'African Rainforest Pavilion' ),
   ( "Grevy's Zebra", 'Canadian Domain' ),
   ( 'Marabou Stork', 'African Rainforest Pavilion' ),
   ( 'Ostrich', 'African Rainforest Pavilion' ),
   ( 'Southern Ground Hornbill', 'African Rainforest Pavilion' ),
   ( 'West Caucasian Tur', 'Indo-Malaya Outdoor' ),
   ( 'White-Headed Vulture', 'African Rainforest Pavilion' ),
}


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare animals listed on the Toronto Zoo website with the animals '
         'in the app.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def clean_website_name( href: str ) -> str:
   return unescape( unquote( href ) ).replace( '+', ' ' ).strip()


def normalize_animal_name( name: str ) -> str:
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


def comparison_key( name: str, use_website_aliases: bool ) -> str:
   normalized = normalize_animal_name( name )

   if use_website_aliases:
      return WEBSITE_NAME_ALIASES.get( normalized, normalized )

   return normalized


def parse_website_animals( page_html: str ) -> list[ tuple[ str, str ] ]:
   names = []
   exhibit = ''

   for match in re.finditer(
         r'(?is)<h1\b[^>]*>(.*?)</h1>|<a href="/animals/([^"]+)" class="thm"',
         page_html ):
      heading, href = match.groups()

      if heading != None:
         exhibit = unescape( re.sub( r'<[^>]+>', ' ', heading ) )
         exhibit = re.sub( r'\s+', ' ', exhibit ).strip()
         continue

      if not exhibit:
         raise RuntimeError( 'An animal listing has no exhibit heading.' )

      name = clean_website_name( href )
      listing = ( exhibit, name )

      if name == '' or listing in names:
         continue

      names.append( listing )

   return names


def fetch_website_animals() -> list[ tuple[ str, str ] ]:
   animals = []

   for path in WEBSITE_REGION_PATHS:
      names = parse_website_animals( fetch_text( f'{ WEBSITE_ANIMALS_URL }/{ path }' ) )

      if not names:
         raise RuntimeError( f'The { path } animals page has no animal list.' )

      animals.extend( names )

   return animals


def load_species( database: Path ) -> list[ tuple[ str, str ] ]:
   connection = sqlite3.connect( f'{ database.resolve().as_uri() }?mode=ro', uri=True )

   try:
      rows = connection.execute(
         """   SELECT COALESCE( Enclosure.EXHIBIT, 'Unassigned exhibit' ), Animal.SPECIES
               FROM Animal
               LEFT JOIN Enclosure ON Enclosure.SPECIES = Animal.SPECIES
         """
      ).fetchall()
   finally:
      connection.close()

   return [ ( str( row[ 0 ] ), str( row[ 1 ] ) ) for row in rows ]


def add_listing(
      listings: dict[ tuple[ str, str ], tuple[ str, list[ str ] ] ],
      exhibit: str,
      name: str,
      use_website_aliases: bool ) -> None:
   key = ( exhibit.casefold(), comparison_key( name, use_website_aliases ) )
   stored = listings.get( key )

   if stored == None:
      listings[ key ] = ( exhibit, [ name ] )
      return

   names = stored[ 1 ]

   if name not in names:
      names.append( name )


def listing_label( names: list[ str ] ) -> str:
   return ' / '.join( sorted( names, key=str.casefold ) )


def missing_labels(
      source: dict[ tuple[ str, str ], tuple[ str, list[ str ] ] ],
      other: dict[ tuple[ str, str ], tuple[ str, list[ str ] ] ] ) -> list[ str ]:
   labels = []

   for key, ( exhibit, names ) in source.items():
      if key in other:
         continue

      labels.append( f'{ listing_label( names ) } · { exhibit }' )

   return sorted( labels, key=str.casefold )


def print_category( title: str, animals: list[ str ] ) -> None:
   print( f'{ title }: { len( animals ) }' )

   for animal in animals:
      print( f'  { animal }' )

   print()


def check_lists( database: Path, today: date ) -> int:
   app_listings: dict[ tuple[ str, str ], tuple[ str, list[ str ] ] ] = {}
   website_listings: dict[ tuple[ str, str ], tuple[ str, list[ str ] ] ] = {}

   for exhibit, species in load_species( database ):
      add_listing( app_listings, exhibit, species, False )

   for exhibit, name in fetch_website_animals():
      add_listing( website_listings, exhibit, name, True )

   website_only = missing_labels( website_listings, app_listings )
   allowed_keys = {
      ( exhibit.casefold(), comparison_key( species, False ) )
      for species, exhibit in ALLOWED_APP_ONLY_ANIMALS
   }
   unapproved_app_listings = {
      key: names
      for key, names in app_listings.items()
      if key not in allowed_keys
   }
   app_only = missing_labels( unapproved_app_listings, website_listings )

   print( f'Animal list check for { today.isoformat() }.' )
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
