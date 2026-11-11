from __future__ import annotations

from datetime import date
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.domain.seasonal_gift_shop import SeasonalGiftShop
from api.request_connection_provider import RequestConnectionProvider
from .gift_shop_card import GiftShopCard
from .gift_shop_listing import GiftShopListing
from .season_window import SeasonWindow
from .website_page import WebsitePage


class SeasonalGiftShopComparison():
   @classmethod
   def parse_website_gift_shops( cls, page_html: str, today: date ) -> list[ str ]:
      return [
         card.title
         for card in GiftShopCard.find( page_html )
         if WebsitePage.is_closed_for_season_status( card.status, today )
      ]


   @classmethod
   def matched_gift_shops(
         cls,
         title: str,
         gift_shops: list[ SeasonalGiftShop ] ) -> list[ SeasonalGiftShop ]:
      website = GiftShopListing( name=title )

      return [
         gift_shop
         for gift_shop in gift_shops
         if GiftShopListing( name=gift_shop.name ) == website
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
   def week_extension_names(
         cls,
         listings: list[ str ],
         gift_shops: list[ SeasonalGiftShop ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            gift_shop.name
            for title in listings
            for gift_shop in cls.matched_gift_shops( title, gift_shops )
            if SeasonWindow.needs_week_extension(
               gift_shop.closed_for_season_on( today ),
               gift_shop.end,
               today,
            )
         },
         key=str.casefold,
      )


   @classmethod
   def missed_unmatched_listings(
         cls,
         listings: list[ str ],
         gift_shops: list[ SeasonalGiftShop ] ) -> list[ str ]:
      return sorted(
         {
            title
            for title in listings
            if not cls.matched_gift_shops( title, gift_shops )
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
