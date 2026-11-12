from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.exhibits.domain.exhibit_season import ExhibitSeason
from api.exhibits.domain.exhibit_season_status import ExhibitSeasonStatus
from api.exhibits.domain.exhibit_species import ExhibitSpecies
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .exhibit_window import ExhibitWindow
from tools.fix.exhibit_season_fixer import ExhibitSeasonFixer
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


class ExhibitSeasonChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalExhibit.description' )
      )


   @classmethod
   def seasons( cls, database: Path ) -> list[ ExhibitSeason ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ExhibitCoordinator.get_exhibit_seasons()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def species_by_exhibit( cls, database: Path ) -> list[ ExhibitSpecies ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ExhibitCoordinator.get_species_by_exhibit()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def statuses( cls, database: Path ) -> list[ ExhibitSeasonStatus ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ExhibitCoordinator.get_season_statuses()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def website_names( cls ) -> set[ str ]:
      return {
         WebsitePage.normalize_name( listing.name )
         for listing in WebsiteOffDisplayAnimal.fetch()
      }


   @classmethod
   def status_for(
         cls,
         statuses: list[ ExhibitSeasonStatus ],
         exhibit: str ) -> ExhibitSeasonStatus | None:
      for status in statuses:
         if status.exhibit == exhibit:
            return status

      return None


   @classmethod
   def species_for( cls, groups: list[ ExhibitSpecies ], exhibit: str ) -> list[ str ]:
      for group in groups:
         if group.exhibit == exhibit:
            return group.species

      return []


   @classmethod
   def closed_on_website( cls, species: list[ str ], names: set[ str ] ) -> bool:
      if not species:
         return False

      return all( WebsitePage.normalize_name( name ) in names for name in species )


   @classmethod
   def lines( cls, database: Path, today: date ) -> list[ str ]:
      seasons = cls.seasons( database )
      species_by_exhibit = cls.species_by_exhibit( database )
      statuses = cls.statuses( database )
      names = cls.website_names()
      lines = []

      for season in sorted( seasons, key=lambda season: season.name.casefold() ):
         exhibit = season.name
         status = cls.status_for( statuses, exhibit )
         website_closed = cls.closed_on_website(
            cls.species_for( species_by_exhibit, exhibit ),
            names,
         )
         window = ExhibitWindow.replacement(
            website_closed,
            status,
            season,
            today,
         )

         if window is None:
            cls.align_closed_animals(
               database,
               exhibit,
               status,
               website_closed,
               today,
            )
            continue

         lines.append( ExhibitSeasonFixer.apply( database, exhibit, window ) )

      return lines


   @classmethod
   def align_closed_animals(
         cls,
         database: Path,
         exhibit: str,
         status: ExhibitSeasonStatus | None,
         website_closed: bool,
         today: date ) -> None:
      if (
         not website_closed
         or status is None
         or not status.closed_for_season
         or status.start is None
         or status.end is None
         or not DateValues.is_date_in_range( today, status.start, status.end )
      ):
         return

      ExhibitSeasonFixer.align_animals( database, exhibit, status.start, status.end )


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
      print( CheckReport.heading( 'seasonalExhibit', today ) )
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
   raise SystemExit( ExhibitSeasonChecker.main() )
