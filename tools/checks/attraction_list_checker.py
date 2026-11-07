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
   def app_listings( cls, attractions: list[ AttractionInfoLink ] ) -> list[ AttractionListing ]:
      return [
         AttractionListing( name=attraction.name, link=attraction.info_link )
         for attraction in attractions
      ]


   @classmethod
   def website_listings( cls, attractions: list[ WebsiteAttraction ] ) -> list[ AttractionListing ]:
      return [
         AttractionListing( name=attraction.title, link=attraction.href )
         for attraction in attractions
         if not AttractionListing( name=attraction.title ).is_website_only()
      ]


   @classmethod
   def missing_names(
         cls,
         source: list[ AttractionListing ],
         other: list[ AttractionListing ] ) -> list[ str ]:
      names = {
         listing.name
         for listing in source
         if not any( listing.matches( candidate ) for candidate in other )
      }

      return sorted( names, key=str.casefold )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_listings = cls.app_listings( cls.load_attractions( database ) )
      website_listings = cls.website_listings( cls.fetch_website_attractions() )
      website_only = cls.missing_names( website_listings, app_listings )
      app_only = cls.missing_names( app_listings, website_listings )

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
