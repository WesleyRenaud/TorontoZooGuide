from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.attractions.data_access.attraction_provider import AttractionProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.date_values import DateValues
from api.shared.enums.item_type import ItemType
from api.types import Types
from .attraction_detail_image import AttractionDetailImage
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .temporary_closure_change import TemporaryClosureChange
from .temporary_closure_check import TemporaryClosureCheck
from .temporary_closure_plan import TemporaryClosurePlan
from .temporary_closure_reader import TemporaryClosureReader
from tools.fix.attraction_temporary_closure_fixer import AttractionTemporaryClosureFixer
from .website_page import WebsitePage


class AttractionTemporaryClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.temporaryAttraction.description' )
      )


   @classmethod
   def stored(
         cls,
         connection: Types.Connection,
         today: date ) -> list[ TemporaryClosureChange ]:
      rows = []

      for record in AttractionProvider.fetch_attraction_schedule_override_records( connection ):
         if not record.is_closed:
            continue

         if not DateValues.is_date_on_or_before( today, record.override_end_date ):
            continue

         rows.append( TemporaryClosureChange(
            record.attraction,
            record.override_message or '',
            ItemType.ATTRACTION,
            TemporaryClosurePlan.as_date( record.override_start_date ),
            TemporaryClosurePlan.as_date( record.override_end_date ),
            AttractionDetailImage.source( record.attraction ),
         ) )

      return rows


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         names = AttractionProvider.fetch_attraction_names( connection )
         stored = cls.stored( connection, today )
      finally:
         connection.close()

      notices = TemporaryClosureReader.read(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) ),
         {
            name: AttractionDetailImage.source( name )
            for name in names
         },
         ItemType.ATTRACTION,
         today,
      )
      plan = TemporaryClosurePlan.build( notices, stored, today )
      AttractionTemporaryClosureFixer.apply( database, plan )
      return TemporaryClosureCheck.run( 'temporaryAttraction', plan, today )


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
   raise SystemExit( AttractionTemporaryClosureChecker.main() )
