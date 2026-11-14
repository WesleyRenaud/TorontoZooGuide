from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from api.animals.status.animal_viewing_alert import AnimalViewingAlert
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.models import Update
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.updates.coordinators.update_coordinator import UpdateCoordinator
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .closure_viewing_alert import ClosureViewingAlert
from tools.fix.closure_viewing_alert_fixer import ClosureViewingAlertFixer
from .viewing_alert_sentence import ViewingAlertSentence


class ClosureViewingAlertChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.closureViewingAlert.description' )
      )


   @classmethod
   def load(
         cls,
         database: Path,
         today: date ) -> tuple[
            list[ Update ],
            list[ AnimalSpeciesExhibit ],
            list[ TemporaryOffDisplayAnimal ],
            list[ AnimalViewingAlert ],
         ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return (
            UpdateCoordinator.get_current_closures( today ),
            AnimalCoordinator.get_animal_species_exhibits(),
            AnimalCoordinator.get_temporary_off_display_animals(),
            AnimalCoordinator.get_animal_viewing_alerts(),
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.removedViewingAlert' ),
         CheckReport.text( 'checks.setViewingAlert' ),
         CheckReport.text( 'checks.updatedViewingAlert' ),
      )
      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      closures, placements, off_display, stored = cls.load( database, today )
      alerts = ClosureViewingAlert.choose(
         closures,
         placements,
         off_display,
         stored,
         today,
      )

      ready = []

      try:
         for alert in alerts:
            alert.message = ViewingAlertSentence.write(
               species=alert.species,
               exhibit=alert.exhibit,
               off_display=alert.off_display,
               scope=alert.scope,
               title=alert.title,
               description=alert.description,
            )

            if alert.message != '' and alert.needs_save( stored ):
               ready.append( alert )
      except RuntimeError as error:
         print( CheckReport.heading( 'closureViewingAlert', today ) )
         print()
         CheckReport.print_category( 'checks.couldNotWriteViewingAlert', [ str( error ) ] )
         return 1

      saved, removed = ClosureViewingAlertFixer.apply(
         database,
         ready,
         ClosureViewingAlert.without_closure( stored, alerts, today ),
      )
      lines = [
         alert.line()
         for alert in sorted( saved, key=lambda alert: alert.sort_key() )
      ]
      removed_lines = [
         ClosureViewingAlert.removal_line( alert )
         for alert in sorted(
            removed,
            key=lambda alert: ( alert.species.casefold(), alert.exhibit.casefold() ),
         )
      ]
      print( CheckReport.heading( 'closureViewingAlert', today ) )
      print()
      CheckReport.print_category( 'checks.animalAlerts', lines )
      CheckReport.print_category( 'checks.appOnly', removed_lines )
      return cls.remaining( lines + removed_lines )


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
   raise SystemExit( ClosureViewingAlertChecker.main() )
