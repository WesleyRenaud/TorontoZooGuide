from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from .animal_catalogue import AnimalCatalogue
from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.animal_visibility_schedule import AnimalVisibilitySchedule
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from tools.fix.viewing_hours_fixer import ViewingHoursFixer
from .viewing_hours import ViewingHours
from .viewing_hours_plan import ViewingHoursPlan
from .website_feature_paths import WebsiteFeaturePaths
from .website_page import WebsitePage
from .website_viewing_hours import WebsiteViewingHours


class ViewingHoursChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.viewingHours.description' )
      )


   @classmethod
   def placements(
         cls,
         database: Path ) -> tuple[
            list[ AnimalSpeciesExhibit ],
            list[ AnimalVisibilitySchedule ],
         ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return (
            AnimalCoordinator.get_animal_species_exhibits(),
            AnimalCoordinator.get_animal_visibility_schedules(),
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def website_hours(
         cls,
         placements: list[ AnimalSpeciesExhibit ] ) -> list[ ViewingHours ]:
      home = WebsitePage.fetch_text( WebsitePage.url( '' ) )
      animals = WebsitePage.fetch_text( WebsitePage.url( AnimalCatalogue.PAGE ) )
      found = []

      for path in WebsiteFeaturePaths.feature_paths( home, animals ):
         page = WebsitePage.fetch_text( WebsitePage.url( path ) )
         found.extend( WebsiteViewingHours.schedules( page, path, placements ) )

      return found


   @classmethod
   def plan( cls, database: Path, today: date ) -> ViewingHoursPlan:
      places, stored = cls.placements( database )
      return ViewingHoursPlan.build( cls.website_hours( places ), stored, today )


   @classmethod
   def ordered( cls, hours: list[ ViewingHours ] ) -> list[ ViewingHours ]:
      return sorted( hours, key=ViewingHours.sort_key )


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setViewingHoursFrom' ),
         CheckReport.text( 'checks.removedViewingHours' ),
         CheckReport.text( 'checks.extendedViewingHoursThrough' ),
         CheckReport.text( 'checks.trimmedViewingHoursThrough' ),
      )
      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      plan = cls.plan( database, today )
      ViewingHoursFixer.apply( database, plan )
      added = [
         item.scheduled_line()
         for item in cls.ordered( plan.added )
      ]
      removed = [
         item.removed_line()
         for item in cls.ordered( plan.removed )
      ]
      extended = [
         item.extended_line()
         for item in cls.ordered( plan.extended )
      ]
      trimmed = [
         item.trimmed_line()
         for item in cls.ordered( plan.trimmed )
      ]
      realigned = [
         item.scheduled_line()
         for item in cls.ordered( plan.realigned )
      ]
      print( CheckReport.heading( 'viewingHours', today ) )
      print()
      CheckReport.print_category( 'checks.websiteOnly', added )
      CheckReport.print_category( 'checks.appOnly', removed )
      CheckReport.print_category(
         'checks.windowsDoNotAlign',
         extended + trimmed + realigned,
      )
      return cls.remaining( added + removed + extended + trimmed + realigned )


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
   raise SystemExit( ViewingHoursChecker.main() )
