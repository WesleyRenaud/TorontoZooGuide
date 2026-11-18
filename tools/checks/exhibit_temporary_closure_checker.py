from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.data_access.exhibit_provider import ExhibitProvider
from api.exhibits.data_access.exhibit_status_provider import ExhibitStatusProvider
from api.shared.date_values import DateValues
from api.shared.enums.item_type import ItemType
from api.shared.text_values import TextValues
from api.types import Types
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .closure_update_builder import ClosureUpdateBuilder
from .date_span import DateSpan
from .exhibit_closure_sentence import ExhibitClosureSentence
from .exhibit_detail_image import ExhibitDetailImage
from .temporary_closure import TemporaryClosure
from .temporary_closure_change import TemporaryClosureChange
from .temporary_closure_check import TemporaryClosureCheck
from .temporary_closure_plan import TemporaryClosurePlan
from .temporary_closure_reader import TemporaryClosureReader
from tools.fix.exhibit_temporary_closure_fixer import ExhibitTemporaryClosureFixer
from .viewing_alert_sentence_builder import ViewingAlertSentenceBuilder
from .website_closure import WebsiteClosure
from .website_page import WebsitePage


class ExhibitTemporaryClosureChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.temporaryExhibit.description' )
      )


   @classmethod
   def stored(
         cls,
         connection: Types.Connection,
         today: date ) -> list[ TemporaryClosureChange ]:
      rows = []

      for record in ExhibitStatusProvider.fetch_closure_records( connection ):
         if record.is_closed_for_season:
            continue

         if not DateValues.is_date_on_or_before( today, record.closed_end ):
            continue

         rows.append( TemporaryClosureChange(
            record.exhibit,
            record.closed_message,
            ItemType.EXHIBIT,
            TemporaryClosurePlan.as_date( record.closed_start ),
            TemporaryClosurePlan.as_date( record.closed_end ),
            ExhibitDetailImage.source( record.exhibit ),
         ) )

      return rows


   @classmethod
   def span( cls, notice: WebsiteClosure, today: date ) -> DateSpan | None:
      days = ClosureUpdateBuilder.dates_named(
         TextValues.beside( notice.title, notice.description ),
         today,
      )
      start = min( days ) if days != [] else today
      end = max( days ) if days != [] else today

      if DateValues.is_date_on_or_before( today, end ):
         return DateSpan( start, end )

      return None


   @classmethod
   def notices(
         cls,
         page_html: str,
         names: list[ str ],
         today: date ) -> list[ TemporaryClosure ]:
      found = {}

      for notice in WebsiteClosure.notices( page_html ):
         span = cls.span( notice, today )

         if span == None:
            continue

         for sentence in ViewingAlertSentenceBuilder.notice_parts(
            TemporaryClosureReader.text( notice ),
         ):
            for name in ExhibitClosureSentence.closed_names( sentence, names ):
               found.setdefault( name, TemporaryClosure(
                  name,
                  sentence,
                  ItemType.EXHIBIT,
                  ExhibitDetailImage.source( name ),
                  span.start,
                  span.end,
               ) )

      return list( found.values() )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         names = ExhibitProvider.fetch_exhibit_names( connection )
         stored = cls.stored( connection, today )
      finally:
         connection.close()

      page = WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      plan = TemporaryClosurePlan.build(
         cls.notices( page, names, today ),
         stored,
         today,
      )
      ExhibitTemporaryClosureFixer.apply( database, plan )
      return TemporaryClosureCheck.run( 'temporaryExhibit', plan, today )


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
   raise SystemExit( ExhibitTemporaryClosureChecker.main() )
