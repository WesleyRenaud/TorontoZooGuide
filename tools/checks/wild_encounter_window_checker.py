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
from tools.fix.wild_encounter_window_fixer import WildEncounterWindowFixer
from .wild_encounter_check import WildEncounterCheck
from .wild_encounter_comparison import WildEncounterComparison


class WildEncounterWindowChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.wildEncounter.description' )
      )


   @classmethod
   def window_detail(
         cls,
         database: Path,
         name: str,
         prepared: WildEncounterCheck ) -> str | None:
      website = WildEncounterComparison.website_schedule( name, prepared )

      if website.failure != None:
         return website.failure

      if website.schedule == None:
         return None

      app = WildEncounterComparison.app_schedule(
         prepared.schedules,
         name,
         prepared.first,
      )

      if website.schedule.matches( app ):
         return None

      return WildEncounterWindowFixer.apply(
         database,
         WildEncounterWindowFixer.correction( name, website.schedule ),
      )


   @classmethod
   def lines( cls, database: Path, prepared: WildEncounterCheck ) -> list[ str ]:
      catalog = { encounter.name for encounter in prepared.encounters }
      names = sorted( prepared.website_names & catalog, key=str.casefold )
      lines = []

      for name in names:
         detail = cls.window_detail( database, name, prepared )

         if detail == None:
            continue

         lines.append( WildEncounterComparison.encounter_line(
            name,
            WildEncounterComparison.region_for( name, prepared.records ),
            [ detail ],
         ) )

      return lines


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      prepared = WildEncounterComparison.prepare( database, today )
      lines = cls.lines( database, prepared )
      CheckReport.report_category(
         'wildEncounter',
         today,
         prepared.note,
         'checks.windowsDoNotAlign',
         lines,
      )
      phrase = CheckReport.text( 'checks.setScheduleFrom' )
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
   raise SystemExit( WildEncounterWindowChecker.main() )
