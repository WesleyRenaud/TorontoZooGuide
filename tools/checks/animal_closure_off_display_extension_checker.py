from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.closure_linked_off_display_animals import ClosureLinkedOffDisplayAnimals
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .closure_update_builder import ClosureUpdateBuilder
from tools.fix.animal_closure_off_display_extension_fixer import AnimalClosureOffDisplayExtensionFixer
from .website_page import WebsitePage
from .website_temporarily_off_display_animal import WebsiteTemporarilyOffDisplayAnimal


class AnimalClosureOffDisplayExtensionChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.closureOffDisplay.description' )
      )


   @classmethod
   def on_website(
         cls,
         species: str,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ] ) -> bool:
      folded = WebsitePage.normalize_name( species )
      return any(
         WebsitePage.normalize_name( listing.name ) == folded
         for listing in listings
      )


   @classmethod
   def load_groups( cls, database: Path ) -> list[ ClosureLinkedOffDisplayAnimals ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ClosureLinkedOffDisplayAnimals.groups(
            AnimalCoordinator.get_closure_linked_off_display_animals()
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def groups_ending_within_the_month(
         cls,
         database: Path,
         today: date ) -> list[ ClosureLinkedOffDisplayAnimals ]:
      groups = cls.load_groups( database )

      if groups == []:
         return []

      listings = WebsiteTemporarilyOffDisplayAnimal.fetch()
      found = []

      for group in groups:
         linked = any(
            cls.on_website( animal.species, listings )
            for animal in group.animals
         )
         animals = [
            animal
            for animal in group.animals
            if ClosureUpdateBuilder.kept_end( animal.end, today ) != animal.end
         ]

         if not linked or animals == []:
            continue

         found.append( ClosureLinkedOffDisplayAnimals( group.title, group.start, animals ) )

      return found


   @classmethod
   def category_lines( cls, database: Path, today: date ) -> list[ str ] | None:
      groups = cls.groups_ending_within_the_month( database, today )

      if groups == []:
         return None

      return AnimalClosureOffDisplayExtensionFixer.fix(
         database,
         groups,
         ClosureUpdateBuilder.horizon( today ),
      )


   @classmethod
   def report( cls, lines: list[ str ] ) -> None:
      CheckReport.print_category( 'checks.closureOffDisplayEndingWithinTheMonth', lines )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.category_lines( database, today )

      if lines == None:
         return 0

      print( CheckReport.heading( 'closureOffDisplay', today ) )
      print()
      cls.report( lines )
      corrected = CheckReport.text( 'checks.extendedOffDisplayThrough' )
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
   raise SystemExit( AnimalClosureOffDisplayExtensionChecker.main() )
