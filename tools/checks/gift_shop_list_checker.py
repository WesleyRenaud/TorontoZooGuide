from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.request_connection_provider import RequestConnectionProvider
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .gift_shop_card import GiftShopCard
from .gift_shop_listing import GiftShopListing
from .website_page import WebsitePage


class GiftShopListChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.giftShopList.description' ) )


   @classmethod
   def parse_website_gift_shops( cls, page_html: str ) -> list[ str ]:
      gift_shops = []

      for card in GiftShopCard.find( page_html ):
         if card.title in gift_shops:
            continue

         gift_shops.append( card.title )

      return gift_shops


   @classmethod
   def fetch_website_gift_shops( cls ) -> list[ str ]:
      return cls.parse_website_gift_shops(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.GIFT_SHOPS ) )
      )


   @classmethod
   def load_gift_shops( cls, database: Path ) -> list[ GiftShopListing ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         names = GiftShopCoordinator.get_gift_shop_names()
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      return [
         GiftShopListing( name=name )
         for name in names
      ]


   @classmethod
   def add_listing( cls, listings: set[ GiftShopListing ], name: str ) -> None:
      listings.add( GiftShopListing( name=name ) )


   @classmethod
   def missing_labels(
         cls,
         source: set[ GiftShopListing ],
         other: set[ GiftShopListing ] ) -> list[ str ]:
      labels = [
         listing.name
         for listing in source
         if listing not in other
      ]

      return sorted( labels, key=str.casefold )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings: set[ GiftShopListing ] = set()
      website_listings: set[ GiftShopListing ] = set()

      for gift_shop in cls.load_gift_shops( database ):
         cls.add_listing( app_listings, gift_shop.name )

      for title in cls.fetch_website_gift_shops():
         cls.add_listing( website_listings, title )

      website_only = cls.missing_labels( website_listings, app_listings )
      app_only = cls.missing_labels( app_listings, website_listings )

      CheckReport.report_differences(
         CheckReport.heading( 'giftShopList', today ),
         website_only,
         app_only,
      )
      return CheckReport.count_differences( website_only, app_only )


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
         issues = cls.check_lists( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( GiftShopListChecker.main() )
