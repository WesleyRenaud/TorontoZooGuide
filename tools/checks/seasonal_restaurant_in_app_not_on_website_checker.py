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
from .seasonal_restaurant_comparison import SeasonalRestaurantComparison
from tools.fix.seasonal_restaurant_open_fixer import SeasonalRestaurantOpenFixer


class SeasonalRestaurantInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalRestaurant.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      restaurants = SeasonalRestaurantComparison.load_seasonal_restaurants( database )
      listings = SeasonalRestaurantComparison.fetch_closed_for_season_restaurants( today )
      lines = SeasonalRestaurantOpenFixer.fix(
         database,
         SeasonalRestaurantComparison.app_only( listings, restaurants, today ),
      )

      print( CheckReport.heading( 'seasonalRestaurant', today ) )
      print()
      CheckReport.print_category( 'checks.closedForSeasonAppOnly', lines )
      corrected = CheckReport.text( 'checks.setOpenForSeason' )
      return sum( corrected not in line for line in lines )


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
         issues = cls.check_schedules( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SeasonalRestaurantInAppNotOnWebsiteChecker.main() )
