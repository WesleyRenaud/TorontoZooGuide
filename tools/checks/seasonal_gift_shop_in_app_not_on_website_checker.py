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
from .seasonal_gift_shop_comparison import SeasonalGiftShopComparison
from tools.fix.seasonal_gift_shop_open_fixer import SeasonalGiftShopOpenFixer


class SeasonalGiftShopInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalGiftShop.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      gift_shops = SeasonalGiftShopComparison.load_seasonal_gift_shops( database )
      listings = SeasonalGiftShopComparison.fetch_closed_for_season_gift_shops( today )
      lines = SeasonalGiftShopOpenFixer.fix(
         database,
         SeasonalGiftShopComparison.app_only( listings, gift_shops, today ),
      )

      print( CheckReport.heading( 'seasonalGiftShop', today ) )
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
   raise SystemExit( SeasonalGiftShopInAppNotOnWebsiteChecker.main() )
