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
from .drinking_fountain_window import DrinkingFountainWindow
from tools.fix.drinking_fountain_window_fixer import DrinkingFountainWindowFixer
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
   def lines( cls, database: Path, today: date ) -> list[ str ]:
      status = cls.load_seasonal_drinking_fountains( database )
      website_closed = cls.fetch_fountains_closed_on_website( today )
      window = DrinkingFountainWindow.replacement( website_closed, status, today )

      if window is None:
         return []

      return [ DrinkingFountainWindowFixer.apply( database, window ) ]


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setClosedForSeasonFrom' ),
         CheckReport.text( 'checks.setOpenForSeasonFrom' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.lines( database, today )
      print( CheckReport.heading( 'seasonalDrinkingFountain', today ) )
      print()
      CheckReport.print_category( 'checks.windowsDoNotAlign', lines )
      return cls.remaining( lines )


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
