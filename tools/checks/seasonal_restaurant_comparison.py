from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import unquote

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.domain.seasonal_restaurant import SeasonalRestaurant
from .restaurant_catalogue import RestaurantCatalogue
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class SeasonalRestaurantComparison():
   @classmethod
   def is_allowed_website_only( cls, title: str ) -> bool:
      normalized = WebsitePage.normalize_name( title )

      return any(
         WebsitePage.normalize_name( name ) == normalized
         for name in RestaurantCatalogue.ALLOWED_WEBSITE_ONLY_RESTAURANTS
      )


   @classmethod
   def parse_website_restaurants( cls, page_html: str, today: date ) -> list[ WebsiteAttraction ]:
      return [
         restaurant
         for restaurant in RestaurantCatalogue.parse_website_restaurants( page_html )
         if WebsitePage.is_closed_for_season_status( restaurant.status, today )
      ]


   @classmethod
   def matched_restaurants(
         cls,
         listing: WebsiteAttraction,
         restaurants: list[ SeasonalRestaurant ] ) -> list[ SeasonalRestaurant ]:
      path = WebsitePage.normalize_path( unquote( listing.href ) )

      return [
         restaurant
         for restaurant in restaurants
         if (
            WebsitePage.normalize_name( restaurant.name ) == WebsitePage.normalize_name( listing.title )
            or (
               path != ''
               and WebsitePage.normalize_path( unquote( restaurant.menu_link ) ) == path
            )
         )
      ]


   @classmethod
   def missed_website_restaurants(
         cls,
         listings: list[ WebsiteAttraction ],
         restaurants: list[ SeasonalRestaurant ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            restaurant.name
            for listing in listings
            for restaurant in cls.matched_restaurants( listing, restaurants )
            if not restaurant.closed_for_season_on( today )
         },
         key=str.casefold,
      )


   @classmethod
   def week_extension_names(
         cls,
         listings: list[ WebsiteAttraction ],
         restaurants: list[ SeasonalRestaurant ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            restaurant.name
            for listing in listings
            for restaurant in cls.matched_restaurants( listing, restaurants )
            if not restaurant.closed_for_season_on( today ) or restaurant.end == today
         },
         key=str.casefold,
      )


   @classmethod
   def missed_unmatched_listings(
         cls,
         listings: list[ WebsiteAttraction ],
         restaurants: list[ SeasonalRestaurant ] ) -> list[ str ]:
      return sorted(
         {
            listing.title
            for listing in listings
            if (
               not cls.is_allowed_website_only( listing.title )
               and not cls.matched_restaurants( listing, restaurants )
            )
         },
         key=str.casefold,
      )


   @classmethod
   def website_restaurant_names(
         cls,
         listings: list[ WebsiteAttraction ],
         restaurants: list[ SeasonalRestaurant ] ) -> set[ str ]:
      names: set[ str ] = set()

      for listing in listings:
         names.update(
            restaurant.name
            for restaurant in cls.matched_restaurants( listing, restaurants )
         )

      return names


   @classmethod
   def fetch_closed_for_season_restaurants( cls, today: date ) -> list[ WebsiteAttraction ]:
      return cls.parse_website_restaurants(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.RESTAURANTS ) ),
         today,
      )


   @classmethod
   def load_seasonal_restaurants( cls, database: Path ) -> list[ SeasonalRestaurant ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return RestaurantCoordinator.get_seasonal_restaurants()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteAttraction ],
         restaurants: list[ SeasonalRestaurant ],
         today: date ) -> list[ str ]:
      names = cls.website_restaurant_names( listings, restaurants )

      return sorted(
         (
            restaurant.name
            for restaurant in restaurants
            if restaurant.closed_for_season_on( today ) and restaurant.name not in names
         ),
         key=str.casefold,
      )
