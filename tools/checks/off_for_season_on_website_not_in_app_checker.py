from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.seasonal_off_display_animal import SeasonalOffDisplayAnimal
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.exhibits.domain.seasonal_exhibit import SeasonalExhibit
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .seasonal_off_display_correction import SeasonalOffDisplayCorrection
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


class OffForSeasonOnWebsiteNotInAppChecker():
   OFF_FOR_SEASON_ON_WEBSITE_NOT_IN_APP_MONTHS = ( 1, 8, 9, 10, 11, 12 )


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalOffDisplay.description' )
      )


   @classmethod
   def covered_by_exhibit(
         cls,
         section: str,
         exhibits: list[ SeasonalExhibit ],
         today: date ) -> bool:
      exhibit = SeasonalExhibit.lookup( section, exhibits )
      return exhibit != None and exhibit.closed_for_season_on( today )


   @classmethod
   def same_animal( cls, website_name: str, app_name: str ) -> bool:
      return WebsitePage.normalize_name( website_name ) == WebsitePage.normalize_name( app_name )


   @classmethod
   def off_in_app(
         cls,
         name: str,
         animals: list[ SeasonalOffDisplayAnimal ],
         today: date ) -> bool:
      return any(
         cls.same_animal( name, animal.name ) and animal.off_for_season_on( today )
         for animal in animals
      )


   @classmethod
   def website_only(
         cls,
         listings: list[ WebsiteOffDisplayAnimal ],
         animals: list[ SeasonalOffDisplayAnimal ],
         exhibits: list[ SeasonalExhibit ],
         today: date ) -> list[ WebsiteOffDisplayAnimal ]:
      return [
         listing
         for listing in listings
         if (
            not cls.covered_by_exhibit( listing.section, exhibits, today )
            and not cls.off_in_app( listing.name, animals, today )
         )
      ]


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
   def load_seasonal_exhibits( cls, database: Path ) -> list[ SeasonalExhibit ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ExhibitCoordinator.get_seasonal_exhibits()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def category_lines( cls, database: Path, today: date ) -> list[ str ] | None:
      if today.month not in cls.OFF_FOR_SEASON_ON_WEBSITE_NOT_IN_APP_MONTHS:
         return None

      animals = cls.load_off_display_animals( database )
      exhibits = cls.load_seasonal_exhibits( database )
      listings = WebsiteOffDisplayAnimal.fetch()
      website_only = cls.website_only( listings, animals, exhibits, today )
      return SeasonalOffDisplayCorrection.correct( database, website_only, today )


   @classmethod
   def report( cls, lines: list[ str ] ) -> None:
      CheckReport.print_category( 'checks.offForSeasonWebsiteOnly', lines )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.category_lines( database, today )

      if lines == None:
         return 0

      print( CheckReport.heading( 'seasonalOffDisplay', today ) )
      print()
      cls.report( lines )
      corrected = CheckReport.text( 'checks.setOffDisplayForSeasonFrom' )
      return sum( corrected not in line for line in lines )


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
   raise SystemExit( OffForSeasonOnWebsiteNotInAppChecker.main() )
