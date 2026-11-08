from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.enclosure_off_display_status import EnclosureOffDisplayStatus
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .temporary_off_display_website_only import TemporaryOffDisplayWebsiteOnly
from tools.fix.temporary_off_display_fixer import TemporaryOffDisplayFixer
from .website_temporarily_off_display_animal import WebsiteTemporarilyOffDisplayAnimal


class TemporaryOffDisplayOnWebsiteNotInAppChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.temporaryOffDisplay.description' )
      )


   @classmethod
   def load_enclosures( cls, database: Path ) -> list[ AnimalSpeciesExhibit ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_animal_species_exhibits()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def load_statuses( cls, database: Path ) -> list[ EnclosureOffDisplayStatus ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_off_display_enclosure_statuses()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def off_display_enclosures(
         cls,
         statuses: list[ EnclosureOffDisplayStatus ],
         today: date ) -> set[ AnimalSpeciesExhibit ]:
      return {
         AnimalSpeciesExhibit( species=status.species, exhibit=status.exhibit )
         for status in statuses
         if status.covers( today )
      }


   @classmethod
   def enclosures_on_display(
         cls,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ],
         enclosures: list[ AnimalSpeciesExhibit ],
         off_display: set[ AnimalSpeciesExhibit ] ) -> list[ AnimalSpeciesExhibit ]:
      return list( dict.fromkeys(
         enclosure
         for listing in listings
         for enclosure in enclosures
         if listing.matches( enclosure ) and enclosure not in off_display
      ) )


   @classmethod
   def unmatched_names(
         cls,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ],
         enclosures: list[ AnimalSpeciesExhibit ] ) -> list[ str ]:
      return [
         listing.name
         for listing in listings
         if not any( listing.matches( enclosure ) for enclosure in enclosures )
      ]


   @classmethod
   def website_only(
         cls,
         listings: list[ WebsiteTemporarilyOffDisplayAnimal ],
         enclosures: list[ AnimalSpeciesExhibit ],
         statuses: list[ EnclosureOffDisplayStatus ],
         today: date ) -> TemporaryOffDisplayWebsiteOnly:
      return TemporaryOffDisplayWebsiteOnly(
         enclosures=cls.enclosures_on_display(
            listings,
            enclosures,
            cls.off_display_enclosures( statuses, today ),
         ),
         unmatched=cls.unmatched_names( listings, enclosures ),
      )


   @classmethod
   def category_lines( cls, database: Path, today: date ) -> list[ str ] | None:
      website_only = cls.website_only(
         WebsiteTemporarilyOffDisplayAnimal.fetch(),
         cls.load_enclosures( database ),
         cls.load_statuses( database ),
         today,
      )

      if website_only.enclosures == [] and website_only.unmatched == []:
         return None

      lines = TemporaryOffDisplayFixer.fix( database, website_only.enclosures, today )
      lines.extend( website_only.unmatched )
      return sorted( lines, key=str.casefold )


   @classmethod
   def report( cls, lines: list[ str ] ) -> None:
      CheckReport.print_category( 'checks.temporaryOffDisplayWebsiteOnly', lines )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.category_lines( database, today )

      if lines == None:
         return 0

      print( CheckReport.heading( 'temporaryOffDisplay', today ) )
      print()
      cls.report( lines )
      corrected = CheckReport.text( 'checks.setOffDisplayThrough' )
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
   raise SystemExit( TemporaryOffDisplayOnWebsiteNotInAppChecker.main() )
