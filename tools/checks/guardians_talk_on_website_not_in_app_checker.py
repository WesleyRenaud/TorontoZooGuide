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


class GuardiansTalkOnWebsiteNotInAppChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.guardiansTalk.description' )
      )


   @classmethod
   def lines( cls, prepared: GuardiansTalkCheck ) -> list[ str ]:
      identities = prepared.website.listings() - prepared.catalog

      return [
         GuardiansTalkComparison.talk_line(
            identity,
            animal=GuardiansTalkComparison.linked_animal( identity, prepared.animals ),
         )
         for identity in sorted( identities, key=GuardiansTalkComparison.label )
      ]


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      prepared = GuardiansTalkComparison.prepare( database, today )
      lines = cls.lines( prepared )
      CheckReport.report_category(
         'guardiansTalk',
         today,
         prepared.note,
         'checks.scheduledOnWebsiteOnly',
         lines,
      )
      return len( lines )


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
   raise SystemExit( GuardiansTalkOnWebsiteNotInAppChecker.main() )
