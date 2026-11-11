from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.models import ZooHours
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .date_span import DateSpan
from tools.fix.zoo_hours_fixer import ZooHoursFixer
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
   def by_day( cls, hours: list[ ZooHours ] ) -> dict[ date, ZooHours ]:
      return {
         date.fromisoformat( item.date ): item
         for item in hours
      }


   @classmethod
   def same_clocks( cls, left: ZooHours, right: ZooHours ) -> bool:
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
         parts.append(
            CheckReport.text( 'checks.earlyAdmission' )
            + DateValues.format_display_time_value( hours.early_admission_time )
         )

      parts.append(
         CheckReport.text( 'checks.openTime' )
         + DateValues.format_display_time_value( hours.open_time )
      )
      parts.append(
         CheckReport.text( 'checks.lastAdmission' )
         + DateValues.format_display_time_value( hours.last_admission_time )
      )
      parts.append(
         CheckReport.text( 'checks.closeTime' )
         + DateValues.format_display_time_value( hours.close_time )
      )
      return AppStringProvider.values()[ 'format.listJoin' ].join( parts )


   @classmethod
   def format_group( cls, span: DateSpan, hours: ZooHours ) -> str:
      formatted = cls.format_hours( hours )

      if span.start == span.end:
         return span.start.isoformat() + CheckReport.text( 'checks.labelValue' ) + formatted

      days = ( span.end - span.start ).days + 1
      return (
         span.start.isoformat()
         + CheckReport.text( 'checks.hoursTo' )
         + span.end.isoformat()
         + CheckReport.text( 'checks.hoursDayCountStart' )
         + str( days )
         + CheckReport.text( 'checks.hoursDayCountEnd' )
         + formatted
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
   def changed_line( cls, app: ZooHours, website: ZooHours ) -> str:
      return CheckReport.join_lines( [
         app.date,
         CheckReport.detail_item(
            CheckReport.text( 'checks.appSchedule' ) + cls.format_hours( app )
         ),
         CheckReport.detail_item(
            CheckReport.text( 'checks.websiteSchedule' ) + cls.format_hours( website )
         ),
         CheckReport.detail_item( CheckReport.text( 'checks.updatedHours' ) ),
      ] )


   @classmethod
   def corrected_groups( cls, hours: list[ ZooHours ], phrase_key: str ) -> list[ str ]:
      detail = CheckReport.detail_item( CheckReport.text( phrase_key ) )

      return [
         CheckReport.join_lines( [ line, detail ] )
         for line in cls.format_groups( hours )
      ]


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setHours' ),
         CheckReport.text( 'checks.removedHours' ),
         CheckReport.text( 'checks.updatedHours' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def only_on_website(
         cls,
         website_by_day: dict[ date, ZooHours ],
         app_by_day: dict[ date, ZooHours ] ) -> list[ ZooHours ]:
      return [
         hours
         for day, hours in website_by_day.items()
         if day not in app_by_day
      ]


   @classmethod
   def different_hours(
         cls,
         website_by_day: dict[ date, ZooHours ],
         app_by_day: dict[ date, ZooHours ] ) -> list[ ZooHours ]:
      return [
         hours
         for day, hours in website_by_day.items()
         if day in app_by_day and not cls.same_clocks( hours, app_by_day[ day ] )
      ]


   @classmethod
   def only_in_app(
         cls,
         website_by_day: dict[ date, ZooHours ],
         app_by_day: dict[ date, ZooHours ] ) -> list[ ZooHours ]:
      return [
         hours
         for day, hours in app_by_day.items()
         if day not in website_by_day
      ]


   @classmethod
   def report(
         cls,
         today: date,
         app_by_day: dict[ date, ZooHours ],
         added: list[ ZooHours ],
         updated: list[ ZooHours ],
         removed: list[ ZooHours ] ) -> int:
      changed = [
         cls.changed_line( app_by_day[ date.fromisoformat( hours.date ) ], hours )
         for hours in sorted( updated, key=lambda hours: hours.date )
      ]
      added_lines = cls.corrected_groups( added, 'checks.setHours' )
      removed_lines = cls.corrected_groups( removed, 'checks.removedHours' )
      print( CheckReport.heading( 'zooHours', today ) )
      print()
      CheckReport.print_category( 'checks.websiteOnly', added_lines )
      CheckReport.print_category( 'checks.differentHours', changed )
      CheckReport.print_category( 'checks.appOnly', removed_lines )
      return cls.remaining( added_lines + changed + removed_lines )


   @classmethod
   def check_lists( cls, database: Path, today: date ) -> int:
      website_by_day = cls.by_day(
         cls.listed_on_or_after( cls.fetch_website_hours( today ), today )
      )
      app_by_day = cls.by_day( cls.load_hours( database, today ) )
      added = cls.only_on_website( website_by_day, app_by_day )
      updated = cls.different_hours( website_by_day, app_by_day )
      removed = cls.only_in_app( website_by_day, app_by_day )
      ZooHoursFixer.apply( database, added + updated, removed )
      return cls.report( today, app_by_day, added, updated, removed )


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
         issues = cls.check_lists( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( ZooHoursChecker.main() )
