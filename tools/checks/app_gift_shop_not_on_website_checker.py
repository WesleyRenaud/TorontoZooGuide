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
from .gift_shop_catalogue import GiftShopCatalogue


class AppGiftShopNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.giftShopList.description' )
      )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings = GiftShopCatalogue.load_gift_shops( database )
      website_listings = GiftShopCatalogue.website_listings(
         GiftShopCatalogue.fetch_website_gift_shops()
      )
      app_only = [
         GiftShopCatalogue.app_line( listing.name )
         for listing in GiftShopCatalogue.missing( app_listings, website_listings )
      ]

      print( CheckReport.heading( 'giftShopList', today ) )
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
   raise SystemExit( AppGiftShopNotOnWebsiteChecker.main() )
