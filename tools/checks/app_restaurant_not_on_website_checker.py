from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .restaurant_catalogue import RestaurantCatalogue


class AppRestaurantNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.restaurantList.description' )
      )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      restaurants = RestaurantCatalogue.load_restaurants( database, today )
      cards = RestaurantCatalogue.fetch_website_restaurants()
      app_only = RestaurantCatalogue.app_only_lines( cards, restaurants )

      print( CheckReport.heading( 'restaurantList', today ) )
      print()
      CheckReport.print_category( 'checks.appOnly', app_only )
      return len( app_only )


   @classmethod
   def main( cls ) -> int:
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
   raise SystemExit( AppRestaurantNotOnWebsiteChecker.main() )
