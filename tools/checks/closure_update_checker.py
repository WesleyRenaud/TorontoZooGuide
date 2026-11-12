from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.models import Update
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.updates.coordinators.update_coordinator import UpdateCoordinator
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .closure_update import ClosureUpdate
from .closure_update_plan import ClosureUpdatePlan
from tools.fix.closure_update_fixer import ClosureUpdateFixer
from .website_closure import WebsiteClosure
from .website_page import WebsitePage


class ClosureUpdateChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.closureUpdate.description' )
      )


   @classmethod
   def active_updates( cls, database: Path, today: date ) -> list[ Update ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return UpdateCoordinator.get_active_updates( today )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def plan( cls, database: Path, today: date ) -> ClosureUpdatePlan:
      notices = WebsiteClosure.closures(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      )
      return ClosureUpdatePlan.build(
         notices,
         cls.active_updates( database, today ),
         today,
      )


   @classmethod
   def lines_for(
         cls,
         updates: list[ ClosureUpdate ],
         line: Callable[ [ ClosureUpdate ], str ] ) -> list[ str ]:
      ordered = sorted( updates, key=lambda update: update.title.casefold() )
      return [ line( update ) for update in ordered ]


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setUpdateFrom' ),
         CheckReport.text( 'checks.endedUpdate' ),
         CheckReport.text( 'checks.extendedUpdateThrough' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      plan = cls.plan( database, today )
      ClosureUpdateFixer.apply( database, plan )
      added = cls.lines_for( plan.added, ClosureUpdate.added_line )
      ended = cls.lines_for( plan.ended, ClosureUpdate.ended_line )
      extended = cls.lines_for( plan.extended, ClosureUpdate.extended_line )
      print( CheckReport.heading( 'closureUpdate', today ) )
      print()
      CheckReport.print_category( 'checks.websiteOnly', added )
      CheckReport.print_category( 'checks.appOnly', ended )
      CheckReport.print_category( 'checks.windowsDoNotAlign', extended )
      return cls.remaining( added + ended + extended )


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
   raise SystemExit( ClosureUpdateChecker.main() )
