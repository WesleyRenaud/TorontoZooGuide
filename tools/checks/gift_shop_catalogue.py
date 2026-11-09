from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.request_connection_provider import RequestConnectionProvider
from .check_report import CheckReport
from .exhibit_region_colors import ExhibitRegionColors
from .gift_shop_card import GiftShopCard
from .gift_shop_detail_image import GiftShopDetailImage
from .gift_shop_listing import GiftShopListing
from .paths import Paths
from .website_page import WebsitePage


class GiftShopCatalogue():
   @classmethod
   def fetch_website_gift_shops( cls ) -> list[ GiftShopCard ]:
      return GiftShopCard.find(
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
   def website_listings( cls, cards: list[ GiftShopCard ] ) -> list[ GiftShopListing ]:
      listings: dict[ GiftShopListing, GiftShopListing ] = {}

      for card in cards:
         listing = GiftShopListing( name=card.title, image=card.image )
         listings.setdefault( listing, listing )

      return list( listings.values() )


   @classmethod
   def app_photo( cls, name: str ) -> str:
      photo = GiftShopDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         return photo

      return ''


   @classmethod
   def photo_line( cls, title: str, photo: str ) -> str:
      if photo == '':
         return title

      return CheckReport.join_lines( [
         title,
         CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo ),
      ] )


   @classmethod
   def app_line( cls, name: str ) -> str:
      return cls.photo_line( ExhibitRegionColors.gift_shop_label( name ), cls.app_photo( name ) )


   @classmethod
   def website_line( cls, listing: GiftShopListing ) -> str:
      return cls.photo_line( listing.name, listing.image )


   @classmethod
   def missing(
         cls,
         source: list[ GiftShopListing ],
         other: list[ GiftShopListing ] ) -> list[ GiftShopListing ]:
      return sorted(
         (
            listing
            for listing in source
            if listing not in other
         ),
         key=lambda listing: listing.name.casefold(),
      )
