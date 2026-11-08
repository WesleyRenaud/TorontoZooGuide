from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.drinking_fountains.domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_page import WebsitePage


class SeasonalDrinkingFountainClosureChecker():
   NOTICES_HEADING_RE = re.compile( r'(?is)<h2[^>]*id="notices"[^>]*>.*?</h2>' )
   ANIMALS_HEADING_RE = re.compile( r'(?is)<h2[^>]*id="animals' )
   BOX_RE = re.compile(
      r'(?is)<div class="box[^"]*"[^>]*>.*?(?=<div class="box|\Z)',
   )
   LEGACY_NOTICE_RE = re.compile( r'(?is)<span>\s*<p>(.*?)</p>' )


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalDrinkingFountain.description' )
      )


   @classmethod
   def notices_section( cls, page_html: str ) -> str:
      heading = cls.NOTICES_HEADING_RE.search( page_html )
      following = cls.ANIMALS_HEADING_RE.search( page_html, heading.end() )
      return page_html[ heading.end():following.start() ]


   @classmethod
   def box_bodies( cls, section: str ) -> list[ str ]:
      return cls.BOX_RE.findall( section )


   @classmethod
   def notice_bodies( cls, page_html: str ) -> list[ str ]:
      section = cls.notices_section( page_html )
      return cls.box_bodies( section ) or cls.LEGACY_NOTICE_RE.findall( section )


   @classmethod
   def fountains_closed_on_website( cls, page_html: str, today: date ) -> bool:
      for body in cls.notice_bodies( page_html ):
         text = WebsitePage.clean_html( body )

         if 'fountain' not in text.casefold():
            continue

         if WebsitePage.is_closed_for_season_status( text, today ):
            return True

      return False


   @classmethod
   def fetch_fountains_closed_on_website( cls, today: date ) -> bool:
      return cls.fountains_closed_on_website(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) ),
         today,
      )


   @classmethod
   def load_seasonal_drinking_fountains( cls, database: Path ) -> SeasonalDrinkingFountains:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return DrinkingFountainCoordinator.get_seasonal_drinking_fountains()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def fountain_name( cls ) -> str:
      return AppStringProvider.format( 'checks.countNames.drinkingFountains' )


   @classmethod
   def closed_in_app( cls, status: SeasonalDrinkingFountains, today: date ) -> bool:
      return status.closed_for_season_on( today )


   @classmethod
   def website_only(
         cls,
         website_closed: bool,
         status: SeasonalDrinkingFountains,
         today: date ) -> list[ str ]:
      if website_closed and not cls.closed_in_app( status, today ):
         return [ cls.fountain_name() ]

      return []


   @classmethod
   def app_only(
         cls,
         website_closed: bool,
         status: SeasonalDrinkingFountains,
         today: date ) -> list[ str ]:
      if cls.closed_in_app( status, today ) and not website_closed:
         return [ cls.fountain_name() ]

      return []


   @classmethod
   def report(
         cls,
         today: date,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( CheckReport.heading( 'seasonalDrinkingFountain', today ) )
      print()
      CheckReport.print_category( 'checks.closedForSeasonWebsiteOnly', website_only )
      CheckReport.print_category( 'checks.closedForSeasonAppOnly', app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      status = cls.load_seasonal_drinking_fountains( database )
      website_closed = cls.fetch_fountains_closed_on_website( today )
      website_only = cls.website_only( website_closed, status, today )
      app_only = cls.app_only( website_closed, status, today )
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
         issues = cls.check_schedules( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SeasonalDrinkingFountainClosureChecker.main() )
