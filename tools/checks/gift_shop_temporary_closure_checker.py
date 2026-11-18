from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.data_access.gift_shop_provider import GiftShopProvider
from api.shared.date_values import DateValues
from api.shared.enums.item_type import ItemType
from api.types import Types
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .gift_shop_detail_image import GiftShopDetailImage
from .temporary_closure_change import TemporaryClosureChange
from .temporary_closure_check import TemporaryClosureCheck
from .temporary_closure_plan import TemporaryClosurePlan
from .temporary_closure_reader import TemporaryClosureReader
from tools.fix.gift_shop_temporary_closure_fixer import GiftShopTemporaryClosureFixer
from .website_page import WebsitePage


class GiftShopTemporaryClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.temporaryGiftShop.description' )
      )


   @classmethod
   def stored(
         cls,
         connection: Types.Connection,
         today: date ) -> list[ TemporaryClosureChange ]:
      rows = []

      for record in GiftShopProvider.fetch_gift_shop_schedule_override_records( connection ):
         if not record.is_closed:
            continue

         if not DateValues.is_date_on_or_before( today, record.override_end_date ):
            continue

         rows.append( TemporaryClosureChange(
            record.gift_shop,
            record.override_message or '',
            ItemType.GIFT_SHOP,
            TemporaryClosurePlan.as_date( record.override_start_date ),
            TemporaryClosurePlan.as_date( record.override_end_date ),
            GiftShopDetailImage.source( record.gift_shop ),
         ) )

      return rows


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         names = GiftShopProvider.fetch_gift_shop_names( connection )
         stored = cls.stored( connection, today )
      finally:
         connection.close()

      notices = TemporaryClosureReader.read(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) ),
         {
            name: GiftShopDetailImage.source( name )
            for name in names
         },
         ItemType.GIFT_SHOP,
         today,
      )
      plan = TemporaryClosurePlan.build( notices, stored, today )
      GiftShopTemporaryClosureFixer.apply( database, plan )
      return TemporaryClosureCheck.run( 'temporaryGiftShop', plan, today )


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
   raise SystemExit( GiftShopTemporaryClosureChecker.main() )
