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


class WebsiteCatalogueNotInAppChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.animalList.description' ) )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings, website_listings = AnimalCatalogue.listings( database )
      website_only = AnimalCatalogue.missing_labels( website_listings, app_listings )

      print( CheckReport.heading( 'animalList', today ) )
      print()
      CheckReport.print_category( 'checks.websiteCatalogueNotInApp', website_only )
      return len( website_only )


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
   raise SystemExit( WebsiteCatalogueNotInAppChecker.main() )
