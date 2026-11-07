from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys
from urllib.parse import unquote

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.domain.seasonal_restaurant import SeasonalRestaurant
from .attraction_card import AttractionCard
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class SeasonalRestaurantClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalRestaurant.description' )
      )


   @classmethod
   def parse_website_restaurants( cls, page_html: str, today: date ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
         )
         for card in AttractionCard.from_openings( page_html )
         if WebsitePage.is_seasonally_closed( card.body, today )
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


   @classmethod
   def report(
         cls,
         today: date,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( CheckReport.heading( 'seasonalRestaurant', today ) )
      print()
      CheckReport.print_category( 'checks.closedForSeasonWebsiteOnly', website_only )
      CheckReport.print_category( 'checks.closedForSeasonAppOnly', app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      restaurants = cls.load_seasonal_restaurants( database )
      listings = cls.fetch_closed_for_season_restaurants( today )
      website_only = cls.missed_website_restaurants( listings, restaurants, today )
      app_only = cls.app_only( listings, restaurants, today )
      cls.report( today, website_only, app_only )
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
         issues = cls.check_schedules( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SeasonalRestaurantClosureChecker.main() )
