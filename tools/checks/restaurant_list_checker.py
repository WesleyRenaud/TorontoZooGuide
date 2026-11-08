from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.models import Restaurant
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.shared.date_values import DateValues
from .attraction_card import AttractionCard
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .restaurants_by_title import RestaurantsByTitle
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class RestaurantListChecker():
   ALLOWED_WEBSITE_ONLY_RESTAURANTS = {
      'Ice Cream Carts',
   }


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.restaurantList.description' ) )


   @classmethod
   def parse_website_restaurants( cls, page_html: str ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
         )
         for card in AttractionCard.from_openings( page_html )
      ]


   @classmethod
   def fetch_website_restaurants( cls ) -> list[ WebsiteAttraction ]:
      return cls.parse_website_restaurants(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.RESTAURANTS ) )
      )


   @classmethod
   def load_restaurants(
         cls,
         database: Path,
         today: date ) -> list[ Restaurant ]:
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
   def name_for_website( cls, title: str, titles: RestaurantsByTitle ) -> str:
      restaurant = titles.restaurant_for( title )

      if restaurant == None:
         return title

      return restaurant.name


   @classmethod
   def missing_labels(
         cls,
         source: set[ str ],
         other: set[ str ] ) -> list[ str ]:
      labels = [
         name
         for name in source
         if name not in other
      ]

      return sorted( labels, key=str.casefold )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      restaurants = cls.load_restaurants( database, today )
      titles = RestaurantsByTitle( restaurants )
      app_listings: set[ str ] = set()
      website_listings: set[ str ] = set()

      for restaurant in restaurants:
         app_listings.add( restaurant.name )

      for website_restaurant in cls.fetch_website_restaurants():
         website_listings.add(
            cls.name_for_website( website_restaurant.title, titles ),
         )

      unapproved_website_listings = {
         name
         for name in website_listings
         if name not in cls.ALLOWED_WEBSITE_ONLY_RESTAURANTS
      }
      website_only = cls.missing_labels( unapproved_website_listings, app_listings )
      app_only = cls.missing_labels( app_listings, website_listings )

      CheckReport.report_differences(
         CheckReport.heading( 'restaurantList', today ),
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
         issues = cls.check_lists( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( RestaurantListChecker.main() )
