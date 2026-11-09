from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .app_restaurant_not_on_website_checker import AppRestaurantNotOnWebsiteChecker
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .restaurant_catalogue import RestaurantCatalogue
from .website_restaurant_not_in_app_checker import WebsiteRestaurantNotInAppChecker


class RestaurantListChecker():
   ALLOWED_WEBSITE_ONLY_RESTAURANTS = RestaurantCatalogue.ALLOWED_WEBSITE_ONLY_RESTAURANTS


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.restaurantList.description' )
      )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      return (
         WebsiteRestaurantNotInAppChecker.check_lists( database, today )
         + AppRestaurantNotOnWebsiteChecker.check_lists( database, today )
      )


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
   raise SystemExit( RestaurantListChecker.main() )
