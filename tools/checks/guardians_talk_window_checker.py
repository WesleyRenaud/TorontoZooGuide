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
from .guardians_talk_check import GuardiansTalkCheck
from .guardians_talk_comparison import GuardiansTalkComparison
from .guardians_talk_listing import GuardiansTalkListing
from tools.fix.guardians_talk_window_fixer import GuardiansTalkWindowFixer


class GuardiansTalkWindowChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.guardiansTalk.description' )
      )


   @classmethod
   def window_detail(
         cls,
         database: Path,
         identity: GuardiansTalkListing,
         prepared: GuardiansTalkCheck ) -> str | None:
      website = GuardiansTalkComparison.week_schedule(
         prepared.website.for_listing( identity ),
      )

      if website == None:
         return None

      app = GuardiansTalkComparison.week_schedule(
         prepared.app.for_listing( identity ),
      )

      if website.matches( app ):
         return None

      return GuardiansTalkWindowFixer.apply(
         database,
         GuardiansTalkWindowFixer.correction(
            identity.name,
            identity.location,
            website,
         ),
      )


   @classmethod
   def lines( cls, database: Path, prepared: GuardiansTalkCheck ) -> list[ str ]:
      identities = prepared.website.listings() & prepared.catalog
      lines = []

      for identity in sorted( identities, key=GuardiansTalkComparison.label ):
         detail = cls.window_detail( database, identity, prepared )

         if detail == None:
            continue

         lines.append( GuardiansTalkComparison.talk_line(
            identity,
            [ detail ],
            GuardiansTalkComparison.linked_animal( identity, prepared.animals ),
         ) )

      return lines


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      prepared = GuardiansTalkComparison.prepare( database, today )
      lines = cls.lines( database, prepared )
      CheckReport.report_category(
         'guardiansTalk',
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
   raise SystemExit( GuardiansTalkWindowChecker.main() )
