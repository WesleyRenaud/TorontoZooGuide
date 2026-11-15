from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.date_values import DateValues
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_route_schedule_provider import TransportationRouteScheduleProvider
from api.transportation.scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from tools.fix.zoomobile_route_fixer import ZoomobileRouteFixer
from .zoomobile_route_builder import ZoomobileRouteBuilder
from .zoomobile_route_reader import ZoomobileRouteReader


class ZoomobileRouteChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.zoomobileRoute.description' )
      )


   @classmethod
   def schedules( cls, database: Path ) -> list[ TransportationCurrentRouteSchedule ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return TransportationRouteScheduleProvider.fetch_transportation_route_schedules(
            connection,
            TransportationName.ZOOMOBILE.value,
         )
      finally:
         connection.close()


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      noticed = ZoomobileRouteReader.read()
      plan = ZoomobileRouteBuilder.build( noticed.route, cls.schedules( database ), today )
      ZoomobileRouteFixer.apply( database, plan )
      lines = []

      if plan.change != None:
         lines.append( plan.change.line() )

      print( CheckReport.heading( 'zoomobileRoute', today ) )
      print()

      if plan.added:
         CheckReport.print_category( 'checks.websiteOnly', lines )
         CheckReport.print_category( 'checks.windowsDoNotAlign', [] )
      else:
         CheckReport.print_category( 'checks.websiteOnly', [] )
         CheckReport.print_category( 'checks.windowsDoNotAlign', lines )

      if lines == []:
         return 0

      phrase = CheckReport.text( 'checks.setRouteTo' )
      return 0 if phrase in lines[ 0 ] else 1


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
   raise SystemExit( ZoomobileRouteChecker.main() )
