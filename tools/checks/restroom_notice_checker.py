from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.restrooms.data_access.restroom_provider import RestroomProvider
from api.restrooms.data_access.restroom_record import RestroomRecord
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .restroom_change import RestroomChange
from .restroom_notice_plan import RestroomNoticePlan
from .restroom_notice_reader import RestroomNoticeReader
from tools.fix.restroom_notice_fixer import RestroomNoticeFixer
from .website_page import WebsitePage


class RestroomNoticeChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.restroom.description' )
      )


   @classmethod
   def records( cls, database: Path ) -> list[ RestroomRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return RestroomProvider.fetch_restroom_records( connection )
      finally:
         connection.close()


   @classmethod
   def plan( cls, database: Path, today: date ) -> RestroomNoticePlan:
      notices = RestroomNoticeReader.read(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      )
      return RestroomNoticePlan.build( notices, cls.records( database ), today )


   @classmethod
   def lines_for(
         cls,
         changes: list[ RestroomChange ],
         line: Callable[ [ RestroomChange ], str ] ) -> list[ str ]:
      ordered = sorted( changes, key=lambda change: change.restroom.casefold() )
      return [ line( change ) for change in ordered ]


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setRestroomFrom' ),
         CheckReport.text( 'checks.setRestroomAlertFrom' ),
         CheckReport.text( 'checks.openedRestroom' ),
         CheckReport.text( 'checks.removedRestroomAlert' ),
         CheckReport.text( 'checks.extendedRestroomThrough' ),
         CheckReport.text( 'checks.extendedRestroomAlertThrough' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      plan = cls.plan( database, today )
      RestroomNoticeFixer.apply( database, plan )
      added = cls.lines_for( plan.added, RestroomChange.added_line )
      ended = cls.lines_for( plan.ended, RestroomChange.ended_line )
      extended = cls.lines_for( plan.extended, RestroomChange.extended_line )
      print( CheckReport.heading( 'restroom', today ) )
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
   raise SystemExit( RestroomNoticeChecker.main() )
