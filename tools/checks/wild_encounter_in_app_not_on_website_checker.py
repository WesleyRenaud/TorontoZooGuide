from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from tools.fix.wild_encounter_in_app_not_on_website_fixer import WildEncounterInAppNotOnWebsiteFixer
from .wild_encounter_check import WildEncounterCheck
from .wild_encounter_comparison import WildEncounterComparison


class WildEncounterInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.wildEncounter.description' )
      )


   @classmethod
   def lines( cls, database: Path, prepared: WildEncounterCheck ) -> list[ str ]:
      names = prepared.app_names - prepared.website_names

      return [
         WildEncounterComparison.encounter_line(
            name,
            WildEncounterComparison.region_for( name, prepared.records ),
            [ WildEncounterInAppNotOnWebsiteFixer.fix( database, name ) ],
         )
         for name in sorted( names, key=str.casefold )
      ]


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      prepared = WildEncounterComparison.prepare( database, today )
      lines = cls.lines( database, prepared )
      CheckReport.report_category(
         'wildEncounter',
         today,
         prepared.note,
         'checks.scheduledInAppOnly',
         lines,
      )
      phrase = CheckReport.text( 'checks.removedSchedule' )
      return sum( phrase not in line for line in lines )


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
   raise SystemExit( WildEncounterInAppNotOnWebsiteChecker.main() )
