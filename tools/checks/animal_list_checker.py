from __future__ import annotations

import argparse
from datetime import date
from html import unescape
from pathlib import Path
import re
import sys

from .animal_listing import AnimalListing
from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_page import WebsitePage


class AnimalListChecker():
   PAGE = 'animals'
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
   WEBSITE_NAME_ALIASES = {
      'wood bison female herd': 'wood bison',
      'wood bison male herd': 'wood bison',
   }
   HEADING_RE = re.compile( r'(?is)<h1\b[^>]*>(?P<title>.*?)</h1>' )
   ANIMAL_LINK_RE = re.compile( r'(?is)<a href="/animals/(?P<name>[^"]+)" class="thm"' )
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


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.animalList.description' ) )


   @classmethod
   def comparison_key( cls, name: str, use_website_aliases: bool ) -> str:
      normalized = WebsitePage.normalize_name( name )

      if use_website_aliases:
         return cls.WEBSITE_NAME_ALIASES.get( normalized, normalized )

      return normalized


   @classmethod
   def parse_website_animals( cls, page_html: str ) -> list[ AnimalSpeciesExhibit ]:
      names = []
      headings = list( cls.HEADING_RE.finditer( page_html ) )
      next_headings = headings[ 1: ]
      next_headings.append( None )

      for heading, next_heading in zip( headings, next_headings ):
         if next_heading == None:
            end = len( page_html )
         else:
            end = next_heading.start()

         exhibit = unescape( re.sub( r'<[^>]+>', ' ', heading.group( 'title' ) ) )
         exhibit = re.sub( r'\s+', ' ', exhibit ).strip()

         for href in cls.ANIMAL_LINK_RE.findall( page_html[ heading.end():end ] ):
            name = WebsitePage.clean_website_name( href )
            listing = AnimalSpeciesExhibit( species=name, exhibit=exhibit )

            if name == '' or listing in names:
               continue

            names.append( listing )

      return names


   @classmethod
   def fetch_website_animals( cls ) -> list[ AnimalSpeciesExhibit ]:
      animals = []

      for path in cls.WEBSITE_REGION_PATHS:
         page = WebsitePage.fetch_text( WebsitePage.url( f'{ cls.PAGE }/{ path }' ) )
         animals.extend( cls.parse_website_animals( page ) )

      return animals


   @classmethod
   def load_species( cls, database: Path ) -> list[ AnimalSpeciesExhibit ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_animal_species_exhibits()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def listing_key(
         cls,
         exhibit: str,
         name: str,
         use_website_aliases: bool ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey(
         species=cls.comparison_key( name, use_website_aliases ),
         exhibit=exhibit,
      )


   @classmethod
   def add_listing(
         cls,
         listings: dict[ SpeciesExhibitKey, AnimalListing ],
         exhibit: str,
         name: str,
         use_website_aliases: bool ) -> None:
      key = cls.listing_key( exhibit, name, use_website_aliases )
      stored = listings.get( key )

      if stored == None:
         listings[ key ] = AnimalListing( exhibit=exhibit, species=[ name ] )
         return

      if name not in stored.species:
         stored.species.append( name )


   @classmethod
   def listing_label( cls, species: list[ str ] ) -> str:
      return ' / '.join( sorted( species, key=str.casefold ) )


   @classmethod
   def missing_labels(
         cls,
         source: dict[ SpeciesExhibitKey, AnimalListing ],
         other: dict[ SpeciesExhibitKey, AnimalListing ] ) -> list[ str ]:
      labels = []

      for key, listing in source.items():
         if key in other:
            continue

         labels.append( AppStringProvider.format(
            'format.middleDotPair',
            first=cls.listing_label( listing.species ),
            second=listing.exhibit,
         ) )

      return sorted( labels, key=str.casefold )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings: dict[ SpeciesExhibitKey, AnimalListing ] = {}
      website_listings: dict[ SpeciesExhibitKey, AnimalListing ] = {}

      for animal in cls.load_species( database ):
         cls.add_listing( app_listings, animal.exhibit, animal.species, False )

      for animal in cls.fetch_website_animals():
         cls.add_listing( website_listings, animal.exhibit, animal.species, True )

      website_only = cls.missing_labels( website_listings, app_listings )
      allowed_keys = {
         cls.listing_key( exhibit, species, False )
         for species, exhibit in cls.ALLOWED_APP_ONLY_ANIMALS
      }
      unapproved_app_listings = {
         key: listing
         for key, listing in app_listings.items()
         if key not in allowed_keys
      }
      app_only = cls.missing_labels( unapproved_app_listings, website_listings )

      CheckReport.report_differences(
         CheckReport.heading( 'animalList', today ),
         website_only,
         app_only,
      )
      return CheckReport.count_differences( website_only, app_only )


   @classmethod
   def main( cls ) -> CheckExitCode:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format( 'checks.couldNotFindDatabase' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_lists( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( AnimalListChecker.main() )
