from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.attractions.data_access.attraction_provider import AttractionProvider
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .attraction_catalogue import AttractionCatalogue
from .attraction_listing import AttractionListing
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .opening_window import OpeningWindow
from tools.fix.attraction_window_fixer import AttractionWindowFixer
from .website_attraction import WebsiteAttraction
from .weekday_window import WeekdayWindow


class AttractionWindowChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.attractionWindow.description' )
      )


   @classmethod
   def load_schedules( cls, database: Path ) -> list[ AttractionScheduleRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return AttractionProvider.fetch_attraction_schedule_records( connection )
      finally:
         connection.close()


   @classmethod
   def listed_names(
         cls,
         item: WebsiteAttraction,
         listings: list[ AttractionListing ] ) -> list[ str ]:
      website = AttractionListing( name=item.title, link=item.href )

      if website.is_website_only():
         return []

      return next(
         (
            [ listing.name ]
            for listing in listings
            if listing.matches( website )
         ),
         [],
      )


   @classmethod
   def load_months( cls, database: Path ) -> dict[ str, PeakMonths ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return AttractionProvider.fetch_peak_months( connection )
      finally:
         connection.close()


   @classmethod
   def report_lines(
         cls,
         database: Path,
         name: str,
         status: str | None,
         schedules: list[ AttractionScheduleRecord ],
         today: date,
         months: PeakMonths ) -> list[ str ]:
      pattern = WeekdayWindow.parse( status )

      if pattern == None:
         return []

      replacement = OpeningWindow.replacement(
         pattern,
         OpeningWindow.covering( schedules, name, today, 'attraction' ),
         today,
         months,
      )

      if replacement == None:
         return []

      return [
         CheckReport.join_lines( [
            AttractionCatalogue.app_line( name ),
            AttractionWindowFixer.apply( database, name, replacement ),
         ] ),
      ]


   @classmethod
   def lines( cls, database: Path, today: date ) -> list[ str ]:
      listings = AttractionCatalogue.app_listings(
         AttractionCatalogue.load_attractions( database )
      )
      schedules = cls.load_schedules( database )
      months = cls.load_months( database )
      seen: set[ str ] = set()
      lines: list[ str ] = []

      for item in AttractionCatalogue.fetch_website_attractions():
         for name in cls.listed_names( item, listings ):
            if name in seen:
               continue

            seen.add( name )
            lines.extend(
               cls.report_lines(
                  database,
                  name,
                  item.status,
                  schedules,
                  today,
                  months.get( name, PeakMonths() ),
               )
            )

      return sorted( lines, key=str.casefold )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      lines = cls.lines( database, today )
      CheckReport.report_category(
         'attractionWindow',
         today,
         OpeningWindow.compared_note( today ),
         'checks.windowsDoNotAlign',
         lines,
      )
      phrase = CheckReport.text( 'checks.setScheduleFrom' )
      return sum( phrase not in line for line in lines )


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
   raise SystemExit( AttractionWindowChecker.main() )
