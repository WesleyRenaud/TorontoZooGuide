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
from .seasonal_attraction_comparison import SeasonalAttractionComparison
from tools.fix.seasonal_attraction_closed_week_fixer import SeasonalAttractionClosedWeekFixer


class SeasonalAttractionRampUpOnWebsiteNotInAppChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalAttraction.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      if today.month in Constants.WEBSITE_NOT_IN_APP_SEASON_MONTHS:
         return 0

      attractions = SeasonalAttractionComparison.load_seasonal_attractions( database )
      listings = SeasonalAttractionComparison.fetch_closed_for_season_attractions( today )
      lines = SeasonalAttractionClosedWeekFixer.fix(
         database,
         today,
         SeasonalAttractionComparison.week_extension_names( listings, attractions, today ),
      )
      unmatched = SeasonalAttractionComparison.missed_unmatched_listings( listings, attractions )

      print( CheckReport.heading( 'seasonalAttraction', today ) )
      print()
      CheckReport.print_category( 'checks.closedForSeasonReturningSoon', lines )
      CheckReport.print_category( 'checks.closedForSeasonWebsiteOnly', unmatched )
      return len( unmatched )


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
   raise SystemExit( SeasonalAttractionRampUpOnWebsiteNotInAppChecker.main() )
