from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from .animal_catalogue import AnimalCatalogue
from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport


class AppCatalogueNotOnWebsiteChecker():
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
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings, website_listings = AnimalCatalogue.listings( database )
      allowed_keys = {
         AnimalCatalogue.listing_key( exhibit, species, False )
         for species, exhibit in cls.ALLOWED_APP_ONLY_ANIMALS
      }
      unapproved_app_listings = {
         key: listing
         for key, listing in app_listings.items()
         if key not in allowed_keys
      }
      app_only = AnimalCatalogue.missing_labels( unapproved_app_listings, website_listings )

      print( CheckReport.heading( 'animalList', today ) )
      print()
      CheckReport.print_category( 'checks.appCatalogueNotOnWebsite', app_only )
      return len( app_only )


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
         issues = cls.check_lists( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( AppCatalogueNotOnWebsiteChecker.main() )
