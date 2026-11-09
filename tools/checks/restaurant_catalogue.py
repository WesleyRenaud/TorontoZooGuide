from __future__ import annotations

from datetime import date
from pathlib import Path
import re

from api.database_connection_provider import DatabaseConnectionProvider
from api.models import Restaurant
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from .attraction_card import AttractionCard
from .check_report import CheckReport
from .exhibit_region_colors import ExhibitRegionColors
from .paths import Paths
from .restaurant_detail_image import RestaurantDetailImage
from .restaurants_by_title import RestaurantsByTitle
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class RestaurantCatalogue():
   ALLOWED_WEBSITE_ONLY_RESTAURANTS = {
      'Ice Cream Carts',
   }
   CARD_IMAGE_RE = re.compile( r'(?is)<img\b[^>]*\bsrc="(?P<src>[^"]+)"' )


   @classmethod
   def card_image( cls, body: str ) -> str:
      return ''.join(
         WebsitePage.absolute_url( match.group( 'src' ) )
         for match in cls.CARD_IMAGE_RE.finditer( body )
      )


   @classmethod
   def parse_website_restaurants( cls, page_html: str ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
            image=cls.card_image( card.body ),
         )
         for card in AttractionCard.from_openings( page_html )
      ]


   @classmethod
   def fetch_website_restaurants( cls ) -> list[ WebsiteAttraction ]:
      return cls.parse_website_restaurants(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.RESTAURANTS ) )
      )


   @classmethod
   def load_restaurants( cls, database: Path, today: date ) -> list[ Restaurant ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return RestaurantCoordinator.get_restaurants(
            day=today.day,
            month=today.month,
            year=today.year,
            include_closed_restaurants=True,
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def resolved_name( cls, title: str, titles: RestaurantsByTitle ) -> str:
      restaurant = titles.restaurant_for( title )

      if restaurant == None:
         return title

      return restaurant.name


   @classmethod
   def app_photo( cls, name: str ) -> str:
      photo = RestaurantDetailImage.source( name )

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
      return cls.photo_line( ExhibitRegionColors.restaurant_label( name ), cls.app_photo( name ) )


   @classmethod
   def website_only_lines(
         cls,
         cards: list[ WebsiteAttraction ],
         restaurants: list[ Restaurant ] ) -> list[ str ]:
      titles = RestaurantsByTitle( restaurants )
      app_names = { restaurant.name for restaurant in restaurants }
      seen: dict[ str, WebsiteAttraction ] = {}

      for card in cards:
         name = cls.resolved_name( card.title, titles )

         if name in cls.ALLOWED_WEBSITE_ONLY_RESTAURANTS or name in app_names:
            continue

         seen.setdefault( name, card )

      return [
         cls.photo_line( name, seen[ name ].image )
         for name in sorted( seen, key=str.casefold )
      ]


   @classmethod
   def app_only_lines(
         cls,
         cards: list[ WebsiteAttraction ],
         restaurants: list[ Restaurant ] ) -> list[ str ]:
      titles = RestaurantsByTitle( restaurants )
      website_names = {
         cls.resolved_name( card.title, titles )
         for card in cards
      }

      return [
         cls.app_line( restaurant.name )
         for restaurant in sorted( restaurants, key=lambda item: item.name.casefold() )
         if restaurant.name not in website_names
      ]
