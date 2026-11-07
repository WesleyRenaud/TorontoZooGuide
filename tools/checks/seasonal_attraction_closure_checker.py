from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.seasonal_attraction import SeasonalAttraction
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .attraction_list_checker import AttractionListChecker
from .attraction_listing import AttractionListing
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class SeasonalAttractionClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalAttraction.description' )
      )


   @classmethod
   def closed_for_season_attractions( cls, page_html: str, today: date ) -> list[ WebsiteAttraction ]:
      return [
         attraction
         for attraction in AttractionListChecker.parse_website_attractions( page_html )
         if WebsitePage.is_closed_for_season_status( attraction.status, today )
      ]


   @classmethod
   def matched_attractions(
         cls,
         listing: WebsiteAttraction,
         attractions: list[ SeasonalAttraction ] ) -> list[ SeasonalAttraction ]:
      website = AttractionListing( name=listing.title, link=listing.href )

      return [
         attraction
         for attraction in attractions
         if AttractionListing( name=attraction.name, link=attraction.info_link ).matches( website )
      ]


   @classmethod
   def missed_website_attractions(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            attraction.name
            for listing in listings
            for attraction in cls.matched_attractions( listing, attractions )
            if not attraction.closed_for_season_on( today )
         },
         key=str.casefold,
      )


   @classmethod
   def missed_unmatched_listings(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ] ) -> list[ str ]:
      return sorted(
         {
            listing.title
            for listing in listings
            if (
               not AttractionListing( name=listing.title ).is_website_only()
               and not cls.matched_attractions( listing, attractions )
            )
         },
         key=str.casefold,
      )


   @classmethod
   def website_attraction_names(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ] ) -> set[ str ]:
      names: set[ str ] = set()

      for listing in listings:
         names.update(
            attraction.name
            for attraction in cls.matched_attractions( listing, attractions )
         )

      return names


   @classmethod
   def fetch_closed_for_season_attractions( cls, today: date ) -> list[ WebsiteAttraction ]:
      return cls.closed_for_season_attractions(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ATTRACTIONS ) ),
         today,
      )


   @classmethod
   def load_seasonal_attractions( cls, database: Path ) -> list[ SeasonalAttraction ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AttractionCoordinator.get_seasonal_attractions()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def website_only(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ],
         today: date ) -> list[ str ]:
      return sorted(
         set( cls.missed_website_attractions( listings, attractions, today ) )
         | set( cls.missed_unmatched_listings( listings, attractions ) ),
         key=str.casefold,
      )


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ],
         today: date ) -> list[ str ]:
      names = cls.website_attraction_names( listings, attractions )

      return sorted(
         (
            attraction.name
            for attraction in attractions
            if attraction.closed_for_season_on( today ) and attraction.name not in names
         ),
         key=str.casefold,
      )


   @classmethod
   def report(
         cls,
         today: date,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( CheckReport.heading( 'seasonalAttraction', today ) )
      print()
      CheckReport.print_category( AppStringProvider.format( 'checks.closedForSeasonWebsiteOnly' ), website_only )
      CheckReport.print_category( AppStringProvider.format( 'checks.closedForSeasonAppOnly' ), app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      attractions = cls.load_seasonal_attractions( database )
      listings = cls.fetch_closed_for_season_attractions( today )
      website_only = cls.website_only( listings, attractions, today )
      app_only = cls.app_only( listings, attractions, today )
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
   raise SystemExit( SeasonalAttractionClosureChecker.main() )
