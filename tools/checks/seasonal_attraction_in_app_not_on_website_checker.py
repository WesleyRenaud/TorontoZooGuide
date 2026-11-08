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
from .seasonal_attraction_comparison import SeasonalAttractionComparison
from tools.fix.seasonal_attraction_open_fixer import SeasonalAttractionOpenFixer


class SeasonalAttractionInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalAttraction.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      attractions = SeasonalAttractionComparison.load_seasonal_attractions( database )
      listings = SeasonalAttractionComparison.fetch_closed_for_season_attractions( today )
      lines = SeasonalAttractionOpenFixer.fix(
         database,
         SeasonalAttractionComparison.app_only( listings, attractions, today ),
      )

      print( CheckReport.heading( 'seasonalAttraction', today ) )
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
   raise SystemExit( SeasonalAttractionInAppNotOnWebsiteChecker.main() )
