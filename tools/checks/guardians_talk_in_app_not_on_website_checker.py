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
from tools.fix.guardians_talk_in_app_not_on_website_fixer import GuardiansTalkInAppNotOnWebsiteFixer


class GuardiansTalkInAppNotOnWebsiteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.guardiansTalk.description' )
      )


   @classmethod
   def lines( cls, database: Path, prepared: GuardiansTalkCheck ) -> list[ str ]:
      identities = prepared.app.listings() - prepared.website.listings()

      return [
         GuardiansTalkComparison.talk_line(
            identity,
            [
               GuardiansTalkInAppNotOnWebsiteFixer.fix(
                  database,
                  identity.name,
                  identity.location,
               ),
            ],
            GuardiansTalkComparison.linked_animal( identity, prepared.animals ),
         )
         for identity in sorted(
            identities,
            key=lambda identity: GuardiansTalkComparison.label(
               identity,
               GuardiansTalkComparison.linked_animal( identity, prepared.animals ),
            ),
         )
      ]


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      prepared = GuardiansTalkComparison.prepare( database, today )
      lines = cls.lines( database, prepared )
      CheckReport.report_category(
         'guardiansTalk',
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
   raise SystemExit( GuardiansTalkInAppNotOnWebsiteChecker.main() )
