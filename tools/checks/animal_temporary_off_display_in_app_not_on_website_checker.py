from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from tools.fix.animal_temporary_on_display_fixer import AnimalTemporaryOnDisplayFixer
from .website_temporarily_off_display_animal import WebsiteTemporarilyOffDisplayAnimal


class AnimalTemporaryOffDisplayInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.temporaryOffDisplay.description' )
      )


   @classmethod
   def load_animals( cls, database: Path ) -> list[ TemporaryOffDisplayAnimal ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_temporary_off_display_animals()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def on_website(
         cls,
         animal: TemporaryOffDisplayAnimal,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ] ) -> bool:
      enclosure = animal.enclosure()
      return any( listing.matches( enclosure ) for listing in listings )


   @classmethod
   def kept_for_closure(
         cls,
         animal: TemporaryOffDisplayAnimal,
         animals: list[ TemporaryOffDisplayAnimal ],
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ] ) -> bool:
      return any(
         animal.shares_closure( other ) and cls.on_website( other, listings )
         for other in animals
      )


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ],
         animals: list[ TemporaryOffDisplayAnimal ],
         today: date ) -> list[ TemporaryOffDisplayAnimal ]:
      current = [
         animal
         for animal in animals
         if animal.covers( today )
      ]
      return [
         animal
         for animal in current
         if (
            not cls.on_website( animal, listings )
            and not cls.kept_for_closure( animal, current, listings )
         )
      ]


   @classmethod
   def category_lines( cls, database: Path, today: date ) -> list[ str ] | None:
      animals = cls.app_only(
         WebsiteTemporarilyOffDisplayAnimal.fetch(),
         cls.load_animals( database ),
         today,
      )

      if animals == []:
         return None

      return AnimalTemporaryOnDisplayFixer.fix( database, animals )


   @classmethod
   def report( cls, lines: list[ str ] ) -> None:
      CheckReport.print_category( 'checks.temporaryOffDisplayAppOnly', lines )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.category_lines( database, today )

      if lines == None:
         return 0

      print( CheckReport.heading( 'temporaryOffDisplay', today ) )
      print()
      cls.report( lines )
      corrected = CheckReport.text( 'checks.setOnDisplay' )
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
   raise SystemExit( AnimalTemporaryOffDisplayInAppNotOnWebsiteChecker.main() )
