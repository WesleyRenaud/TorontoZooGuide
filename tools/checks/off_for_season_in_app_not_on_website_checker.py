from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.seasonal_off_display_animal import SeasonalOffDisplayAnimal
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


class OffForSeasonInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalOffDisplay.description' )
      )


   @classmethod
   def same_animal( cls, website_name: str, app_name: str ) -> bool:
      return WebsitePage.normalize_name( website_name ) == WebsitePage.normalize_name( app_name )


   @classmethod
   def listed_on_website( cls, name: str, listings: list[ WebsiteOffDisplayAnimal ] ) -> bool:
      return any( cls.same_animal( listing.name, name ) for listing in listings )


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteOffDisplayAnimal ],
         animals: list[ SeasonalOffDisplayAnimal ],
         today: date ) -> list[ str ]:
      names = {
         animal.name
         for animal in animals
         if animal.off_for_season_on( today ) and not cls.listed_on_website( animal.name, listings )
      }
      return sorted( names, key=str.casefold )


   @classmethod
   def load_off_display_animals( cls, database: Path ) -> list[ SeasonalOffDisplayAnimal ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_seasonal_off_display_animals()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def category_lines( cls, database: Path, today: date ) -> list[ str ]:
      animals = cls.load_off_display_animals( database )
      listings = WebsiteOffDisplayAnimal.fetch()
      return cls.app_only( listings, animals, today )


   @classmethod
   def report( cls, app_only: list[ str ] ) -> None:
      CheckReport.print_category( 'checks.offForSeasonAppOnly', app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      app_only = cls.category_lines( database, today )
      print( CheckReport.heading( 'seasonalOffDisplay', today ) )
      print()
      cls.report( app_only )
      return len( app_only )


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
   raise SystemExit( OffForSeasonInAppNotOnWebsiteChecker.main() )
