from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.events.coordinators.event_coordinator import EventCoordinator
from api.models import Event
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from tools.fix.zoo_event_fixer import ZooEventFixer
from .website_page import WebsitePage
from .website_zoo_event import WebsiteZooEvent


class ZooEventChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.zooEvent.description' ) )


   @classmethod
   def load( cls, database: Path ) -> list[ Event ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return EventCoordinator.get_events()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def missing(
         cls,
         website: list[ WebsiteZooEvent ],
         stored: list[ Event ] ) -> tuple[ list[ WebsiteZooEvent ], list[ WebsiteZooEvent ] ]:
      names = { event.name for event in stored }
      added = []
      unread = []

      for event in website:
         if event.name in names:
            continue

         if event.start == None:
            unread.append( event )
         else:
            added.append( event )

      return added, unread


   @classmethod
   def current( cls, event: Event, today: date ) -> bool:
      if event.end_date == None or str( event.end_date ).strip() == '':
         return True

      return DateValues.parse_date_value( event.end_date ) >= today


   @classmethod
   def extra(
         cls,
         website: list[ WebsiteZooEvent ],
         stored: list[ Event ],
         today: date ) -> list[ Event ]:
      names = { event.name for event in website }
      return [
         event
         for event in stored
         if event.name not in names and cls.current( event, today )
      ]


   @classmethod
   def line( cls, name: str, detail: str ) -> str:
      return CheckReport.join_lines( [
         name,
         CheckReport.detail_item( detail ),
      ] )


   @classmethod
   def added_line( cls, event: WebsiteZooEvent ) -> str:
      details = []

      if event.image != '':
         details.append( CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + event.image ) )

      details.append( CheckReport.detail_item( CheckReport.text( 'checks.addedZooEvent' ) ) )

      if event.description != '':
         details.append( CheckReport.detail_item( event.description ) )

      return CheckReport.join_lines( [ event.name, *details ] )


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.addedZooEvent' ),
         CheckReport.text( 'checks.removedZooEvent' ),
      )
      return sum( all( phrase not in line for phrase in phrases ) for line in lines )


   @classmethod
   def check_schedules(
         cls,
         database: Path,
         today: date,
         home_html: str | None = None,
         pages: dict[ str, str ] | None = None ) -> int:
      if home_html == None:
         home_html = WebsitePage.fetch_text( WebsitePage.BASE_URL )

      website = WebsiteZooEvent.read( home_html, today, pages )
      stored = cls.load( database )
      added, unread = cls.missing( website, stored )
      extra = cls.extra( website, stored, today )
      saved, removed = ZooEventFixer.apply( database, added, extra )
      added_lines = [
         cls.added_line( event )
         for event in saved
      ]
      unread_lines = [
         cls.line( event.name, CheckReport.text( 'checks.couldNotReadZooEventDates' ) )
         for event in unread
      ]
      removed_lines = [
         cls.line( event.name, CheckReport.text( 'checks.removedZooEvent' ) )
         for event in removed
      ]
      lines = added_lines + unread_lines + removed_lines
      print( CheckReport.heading( 'zooEvent', today ) )
      print()
      CheckReport.print_category( 'checks.websiteOnly', added_lines + unread_lines )
      CheckReport.print_category( 'checks.appOnly', removed_lines )
      return cls.remaining( lines )


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
   raise SystemExit( ZooEventChecker.main() )
