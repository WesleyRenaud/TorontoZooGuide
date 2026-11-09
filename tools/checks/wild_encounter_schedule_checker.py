from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .wild_encounter_in_app_not_on_website_checker import WildEncounterInAppNotOnWebsiteChecker
from .wild_encounter_on_website_not_in_app_checker import WildEncounterOnWebsiteNotInAppChecker
from .wild_encounter_window_checker import WildEncounterWindowChecker


class WildEncounterScheduleChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.wildEncounter.description' )
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      return (
         WildEncounterInAppNotOnWebsiteChecker.check_schedules( database, today )
         + WildEncounterOnWebsiteNotInAppChecker.check_schedules( database, today )
         + WildEncounterWindowChecker.check_schedules( database, today )
      )


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
   raise SystemExit( WildEncounterScheduleChecker.main() )
