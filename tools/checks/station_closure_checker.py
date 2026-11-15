from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.date_values import DateValues
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_station_status_provider import TransportationStationStatusProvider
from api.transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .station_change import StationChange
from .station_closure_plan import StationClosurePlan
from .station_closure_reader import StationClosureReader
from tools.fix.station_closure_fixer import StationClosureFixer
from .website_page import WebsitePage


class StationClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.stationClosure.description' )
      )


   @classmethod
   def records( cls, database: Path ) -> list[ TransportationStationStatusRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return TransportationStationStatusProvider.fetch_transportation_station_status_records(
            connection,
            TransportationName.ZOOMOBILE.value,
         )
      finally:
         connection.close()


   @classmethod
   def plan( cls, database: Path, today: date ) -> StationClosurePlan:
      notices = StationClosureReader.read(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) ),
         today,
      )
      return StationClosurePlan.build( notices, cls.records( database ), today )


   @classmethod
   def lines_for(
         cls,
         changes: list[ StationChange ],
         line: Callable[ [ StationChange ], str ] ) -> list[ str ]:
      ordered = sorted( changes, key=lambda change: change.station.casefold() )
      return [ line( change ) for change in ordered ]


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setStationFrom' ),
         CheckReport.text( 'checks.openedStation' ),
         CheckReport.text( 'checks.extendedStationThrough' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      plan = cls.plan( database, today )
      StationClosureFixer.apply( database, plan )
      added = cls.lines_for( plan.added, StationChange.added_line )
      ended = cls.lines_for( plan.ended, StationChange.ended_line )
      extended = cls.lines_for( plan.extended, StationChange.extended_line )
      print( CheckReport.heading( 'stationClosure', today ) )
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
   raise SystemExit( StationClosureChecker.main() )
