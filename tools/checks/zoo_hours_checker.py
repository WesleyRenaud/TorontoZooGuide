from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.models import ZooHours
from api.request_connection_provider import RequestConnectionProvider
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .date_span import DateSpan
from .website_page import WebsitePage
from .zoo_hours_page import ZooHoursPage


class ZooHoursChecker():
   PAGE = 'plan'


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.zooHours.description' )
      )


   @classmethod
   def fetch_website_hours( cls, today: date ) -> list[ ZooHours ]:
      return ZooHoursPage.parse( WebsitePage.fetch_text( WebsitePage.url( cls.PAGE ) ), today )


   @classmethod
   def load_hours( cls, database: Path, today: date ) -> list[ ZooHours ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ZooHoursCoordinator.get_zoo_hours_on_or_after( today )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def listed_on_or_after( cls, hours: list[ ZooHours ], today: date ) -> list[ ZooHours ]:
      return [
         item
         for item in hours
         if date.fromisoformat( item.date ) >= today
      ]


   @classmethod
   def hours_on( cls, day: date, hours: list[ ZooHours ] ) -> ZooHours | None:
      key = day.isoformat()

      for item in hours:
         if item.date == key:
            return item

      return None


   @classmethod
   def same_clocks( cls, left: ZooHours | None, right: ZooHours | None ) -> bool:
      if left == None or right == None:
         return left == right

      return (
         left.early_admission_time == right.early_admission_time
         and left.open_time == right.open_time
         and left.last_admission_time == right.last_admission_time
         and left.close_time == right.close_time
      )


   @classmethod
   def format_hours( cls, hours: ZooHours ) -> str:
      parts = []

      if hours.early_admission_time != None:
         parts.append( AppStringProvider.format(
            'checks.earlyAdmission',
            time=hours.early_admission_time,
         ) )

      parts.append( AppStringProvider.format( 'checks.openTime', time=hours.open_time ) )
      parts.append( AppStringProvider.format(
         'checks.lastAdmission',
         time=hours.last_admission_time,
      ) )
      parts.append( AppStringProvider.format( 'checks.closeTime', time=hours.close_time ) )
      return AppStringProvider.values()[ 'format.listJoin' ].join( parts )


   @classmethod
   def format_group( cls, span: DateSpan, hours: ZooHours ) -> str:
      formatted = cls.format_hours( hours )

      if span.start == span.end:
         return AppStringProvider.format(
            'checks.hoursDay',
            day=span.start.isoformat(),
            hours=formatted,
         )

      return AppStringProvider.format(
         'checks.hoursSpan',
         start=span.start.isoformat(),
         end=span.end.isoformat(),
         days=( span.end - span.start ).days + 1,
         hours=formatted,
      )


   @classmethod
   def format_groups( cls, hours: list[ ZooHours ] ) -> list[ str ]:
      lines = []
      span = None
      current = None

      for item in sorted( hours, key=lambda item: item.date ):
         day = date.fromisoformat( item.date )

         if (
            span != None
            and current != None
            and span.is_next_day( day )
            and cls.same_clocks( current, item )
         ):
            span = span.extended_to( day )
            continue

         if span != None and current != None:
            lines.append( cls.format_group( span, current ) )

         span = DateSpan( start=day, end=day )
         current = item

      if span != None and current != None:
         lines.append( cls.format_group( span, current ) )

      return lines


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      app_hours = cls.load_hours( database, today )
      website_hours = cls.listed_on_or_after( cls.fetch_website_hours( today ), today )
      days = sorted( {
         date.fromisoformat( item.date )
         for item in website_hours + app_hours
      } )
      website_only = []
      app_only = []

      for day in days:
         website = cls.hours_on( day, website_hours )
         app = cls.hours_on( day, app_hours )

         if cls.same_clocks( website, app ):
            continue

         if website != None:
            website_only.append( website )

         if app != None:
            app_only.append( app )

      website_groups = cls.format_groups( website_only )
      app_groups = cls.format_groups( app_only )
      CheckReport.report_differences(
         CheckReport.heading( 'zooHours', today ),
         website_groups,
         app_groups,
      )
      return CheckReport.count_differences( website_groups, app_groups )


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format(
               'checks.couldNotFindDatabase',
               database=args.database,
            ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_lists( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( ZooHoursChecker.main() )
