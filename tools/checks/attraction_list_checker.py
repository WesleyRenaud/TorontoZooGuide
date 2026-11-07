from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.attraction_info_link import AttractionInfoLink
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .attraction_card import AttractionCard
from .attraction_listing import AttractionListing
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class AttractionListChecker():
   ALLOWED_WEBSITE_ONLY_ATTRACTIONS = {
      'Kids Zoo',
      "Nature's Night Shift",
      'Serengeti Bush Camp',
   }


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.attractionList.description' )
      )


   @classmethod
   def website_attractions( cls, cards: list[ AttractionCard ] ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
         )
         for card in cards
      ]


   @classmethod
   def parse_website_attractions( cls, page_html: str ) -> list[ WebsiteAttraction ]:
      return cls.website_attractions( AttractionCard.find( page_html ) )


   @classmethod
   def fetch_website_attractions( cls ) -> list[ WebsiteAttraction ]:
      return cls.parse_website_attractions(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ATTRACTIONS ) )
      )


   @classmethod
   def load_attractions( cls, database: Path ) -> list[ AttractionInfoLink ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AttractionCoordinator.get_attraction_info_links()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def add_listing( cls, listings: set[ AttractionListing ], name: str ) -> None:
      listings.add( AttractionListing( name=name ) )


   @classmethod
   def missing_labels(
         cls,
         source: set[ AttractionListing ],
         other: set[ AttractionListing ] ) -> list[ str ]:
      labels = [
         listing.name
         for listing in source
         if listing not in other
      ]

      return sorted( labels, key=str.casefold )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings: set[ AttractionListing ] = set()
      website_listings: set[ AttractionListing ] = set()

      for attraction in cls.load_attractions( database ):
         cls.add_listing( app_listings, attraction.name )

      for attraction in cls.fetch_website_attractions():
         cls.add_listing( website_listings, attraction.title )

      allowed_listings = {
         AttractionListing( name=name )
         for name in cls.ALLOWED_WEBSITE_ONLY_ATTRACTIONS
      }
      unapproved_website_listings = {
         listing
         for listing in website_listings
         if listing not in allowed_listings
      }
      website_only = cls.missing_labels( unapproved_website_listings, app_listings )
      app_only = cls.missing_labels( app_listings, website_listings )

      CheckReport.report_differences(
         CheckReport.heading( 'attractionList', today ),
         website_only,
         app_only,
      )
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
         issues = cls.check_lists( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( AttractionListChecker.main() )
