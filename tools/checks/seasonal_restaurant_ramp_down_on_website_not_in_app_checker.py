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
from .constants import Constants
from .seasonal_restaurant_comparison import SeasonalRestaurantComparison
from tools.fix.seasonal_restaurant_closed_until_month_fixer import SeasonalRestaurantClosedUntilMonthFixer


class SeasonalRestaurantRampDownOnWebsiteNotInAppChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalRestaurant.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      if today.month not in Constants.WEBSITE_NOT_IN_APP_SEASON_MONTHS:
         return 0

      restaurants = SeasonalRestaurantComparison.load_seasonal_restaurants( database )
      listings = SeasonalRestaurantComparison.fetch_closed_for_season_restaurants( today )
      matched = SeasonalRestaurantComparison.missed_website_restaurants(
         listings,
         restaurants,
         today,
      )
      unmatched = SeasonalRestaurantComparison.missed_unmatched_listings( listings, restaurants )
      lines = SeasonalRestaurantClosedUntilMonthFixer.fix( database, today, matched ) + unmatched

      print( CheckReport.heading( 'seasonalRestaurant', today ) )
      print()
      CheckReport.print_category( 'checks.closedForSeasonWebsiteOnly', lines )
      corrected = CheckReport.text( 'checks.setClosedForSeasonFrom' )
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
   raise SystemExit( SeasonalRestaurantRampDownOnWebsiteNotInAppChecker.main() )
