from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.domain.seasonal_gift_shop import SeasonalGiftShop
from api.request_connection_provider import RequestConnectionProvider
from .attraction_card import AttractionCard
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .gift_shop_card import GiftShopCard
from .website_page import WebsitePage


class SeasonalGiftShopClosureChecker():
   TITLE_OPENING_RE = re.compile( r'(?is)<strong>' )
   TITLE_CLOSING_RE = re.compile( r'(?is)</strong>' )


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalGiftShop.description' )
      )


   @classmethod
   def visible_page_html( cls, page_html: str ) -> str:
      return re.sub( r'(?is)<!--.*?-->', '', page_html )


   @classmethod
   def title( cls, body: str ) -> str:
      opening = cls.TITLE_OPENING_RE.search( body )
      closing = cls.TITLE_CLOSING_RE.search( body, opening.end() )
      return WebsitePage.clean_html( body[ opening.end():closing.start() ] )


   @classmethod
   def cards( cls, page_html: str ) -> list[ GiftShopCard ]:
      page_html = cls.visible_page_html( page_html )
      cards = []

      for card in AttractionCard.from_openings( page_html ):
         cards.append( GiftShopCard(
            title=cls.title( card.body ),
            status=WebsitePage.opening_status( card.body ),
         ) )

      return cards


   @classmethod
   def parse_website_gift_shops( cls, page_html: str, today: date ) -> list[ str ]:
      return [
         card.title
         for card in cls.cards( page_html )
         if WebsitePage.is_closed_for_season_status( card.status, today )
      ]


   @classmethod
   def matched_gift_shops(
         cls,
         title: str,
         gift_shops: list[ SeasonalGiftShop ] ) -> list[ SeasonalGiftShop ]:
      folded = title.casefold()

      return [
         gift_shop
         for gift_shop in gift_shops
         if gift_shop.name.casefold() == folded
      ]


   @classmethod
   def missed_website_gift_shops(
         cls,
         listings: list[ str ],
         gift_shops: list[ SeasonalGiftShop ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            gift_shop.name
            for title in listings
            for gift_shop in cls.matched_gift_shops( title, gift_shops )
            if not gift_shop.closed_for_season_on( today )
         },
         key=str.casefold,
      )


   @classmethod
   def website_gift_shop_names(
         cls,
         listings: list[ str ],
         gift_shops: list[ SeasonalGiftShop ] ) -> set[ str ]:
      names: set[ str ] = set()

      for title in listings:
         names.update(
            gift_shop.name
            for gift_shop in cls.matched_gift_shops( title, gift_shops )
         )

      return names


   @classmethod
   def fetch_closed_for_season_gift_shops( cls, today: date ) -> list[ str ]:
      return cls.parse_website_gift_shops(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.GIFT_SHOPS ) ),
         today,
      )


   @classmethod
   def load_seasonal_gift_shops( cls, database: Path ) -> list[ SeasonalGiftShop ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return GiftShopCoordinator.get_seasonal_gift_shops()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def app_only(
         cls,
         listings: list[ str ],
         gift_shops: list[ SeasonalGiftShop ],
         today: date ) -> list[ str ]:
      names = cls.website_gift_shop_names( listings, gift_shops )

      return sorted(
         (
            gift_shop.name
            for gift_shop in gift_shops
            if gift_shop.closed_for_season_on( today ) and gift_shop.name not in names
         ),
         key=str.casefold,
      )


   @classmethod
   def report(
         cls,
         today: date,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( CheckReport.heading( 'seasonalGiftShop', today ) )
      print()
      CheckReport.print_category( AppStringProvider.format( 'checks.closedForSeasonWebsiteOnly' ), website_only )
      CheckReport.print_category( AppStringProvider.format( 'checks.closedForSeasonAppOnly' ), app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      gift_shops = cls.load_seasonal_gift_shops( database )
      listings = cls.fetch_closed_for_season_gift_shops( today )
      website_only = cls.missed_website_gift_shops( listings, gift_shops, today )
      app_only = cls.app_only( listings, gift_shops, today )
      cls.report( today, website_only, app_only )
      return CheckReport.count_differences( website_only, app_only )


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format(
               'checks.couldNotFindDatabase',
               database=args.database,
            ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_schedules( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SeasonalGiftShopClosureChecker.main() )
