from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.data_access.gift_shop_provider import GiftShopProvider
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .gift_shop_card import GiftShopCard
from .gift_shop_catalogue import GiftShopCatalogue
from .gift_shop_listing import GiftShopListing
from .opening_window import OpeningWindow
from tools.fix.gift_shop_window_fixer import GiftShopWindowFixer
from .weekday_window import WeekdayWindow


class GiftShopWindowChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.giftShopWindow.description' )
      )


   @classmethod
   def load_schedules( cls, database: Path ) -> list[ GiftShopScheduleRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return GiftShopProvider.fetch_gift_shop_schedule_records( connection )
      finally:
         connection.close()


   @classmethod
   def listed_names(
         cls,
         card: GiftShopCard,
         listings: list[ GiftShopListing ] ) -> list[ str ]:
      website = GiftShopListing( name=card.title )
      return next(
         (
            [ listing.name ]
            for listing in listings
            if listing == website
         ),
         [],
      )


   @classmethod
   def load_months( cls, database: Path ) -> dict[ str, PeakMonths ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return GiftShopProvider.fetch_peak_months( connection )
      finally:
         connection.close()


   @classmethod
   def report_lines(
         cls,
         database: Path,
         name: str,
         status: str | None,
         schedules: list[ GiftShopScheduleRecord ],
         today: date,
         months: PeakMonths ) -> list[ str ]:
      pattern = WeekdayWindow.parse( status )

      if pattern == None:
         return []

      replacement = OpeningWindow.replacement(
         pattern,
         OpeningWindow.covering( schedules, name, today, 'gift_shop' ),
         today,
         months,
      )

      if replacement == None:
         return []

      return [
         CheckReport.join_lines( [
            GiftShopCatalogue.app_line( name ),
            GiftShopWindowFixer.apply( database, name, replacement ),
         ] ),
      ]


   @classmethod
   def lines( cls, database: Path, today: date ) -> list[ str ]:
      listings = GiftShopCatalogue.load_gift_shops( database )
      schedules = cls.load_schedules( database )
      months = cls.load_months( database )
      seen: set[ str ] = set()
      lines: list[ str ] = []

      for card in GiftShopCatalogue.fetch_website_gift_shops():
         for name in cls.listed_names( card, listings ):
            if name in seen:
               continue

            seen.add( name )
            lines.extend(
               cls.report_lines(
                  database,
                  name,
                  card.status,
                  schedules,
                  today,
                  months.get( name, PeakMonths() ),
               )
            )

      return sorted( lines, key=str.casefold )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.lines( database, today )
      CheckReport.report_category(
         'giftShopWindow',
         today,
         OpeningWindow.compared_note( today ),
         'checks.windowsDoNotAlign',
         lines,
      )
      phrase = CheckReport.text( 'checks.setScheduleFrom' )
      return sum( phrase not in line for line in lines )


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
   raise SystemExit( GiftShopWindowChecker.main() )
