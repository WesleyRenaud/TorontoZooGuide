from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant_provider import RestaurantProvider
from api.restaurants.data_access.restaurant_schedule_record import RestaurantScheduleRecord
from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .opening_window import OpeningWindow
from .restaurant_catalogue import RestaurantCatalogue
from tools.fix.restaurant_window_fixer import RestaurantWindowFixer
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage
from .weekday_window import WeekdayWindow


class RestaurantWindowChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.restaurantWindow.description' )
      )


   @classmethod
   def load_names( cls, database: Path ) -> list[ str ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return RestaurantCoordinator.get_restaurant_names()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def load_schedules( cls, database: Path ) -> list[ RestaurantScheduleRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return RestaurantProvider.fetch_restaurant_schedule_records( connection )
      finally:
         connection.close()


   @classmethod
   def listed_names(
         cls,
         card: WebsiteAttraction,
         names: list[ str ] ) -> list[ str ]:
      folded = WebsitePage.normalize_name( card.title )
      return next(
         (
            [ name ]
            for name in names
            if WebsitePage.normalize_name( name ) == folded
         ),
         [],
      )


   @classmethod
   def load_months( cls, database: Path ) -> dict[ str, PeakMonths ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return RestaurantProvider.fetch_peak_months( connection )
      finally:
         connection.close()


   @classmethod
   def report_lines(
         cls,
         database: Path,
         name: str,
         status: str | None,
         schedules: list[ RestaurantScheduleRecord ],
         today: date,
         months: PeakMonths ) -> list[ str ]:
      pattern = WeekdayWindow.parse( status )

      if pattern == None:
         return []

      replacement = OpeningWindow.replacement(
         pattern,
         OpeningWindow.covering( schedules, name, today, 'restaurant' ),
         today,
         months,
      )

      if replacement == None:
         return []

      return [
         CheckReport.join_lines( [
            RestaurantCatalogue.app_line( name ),
            RestaurantWindowFixer.apply( database, name, replacement ),
         ] ),
      ]


   @classmethod
   def lines( cls, database: Path, today: date ) -> list[ str ]:
      names = cls.load_names( database )
      schedules = cls.load_schedules( database )
      months = cls.load_months( database )
      seen: set[ str ] = set()
      lines: list[ str ] = []

      for card in RestaurantCatalogue.fetch_website_restaurants():
         for name in cls.listed_names( card, names ):
            if name in seen:
               continue

            seen.add( name )
            lines.extend(
               cls.report_lines(
                  database,
                  name,
                  card.status,
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
         'restaurantWindow',
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
   raise SystemExit( RestaurantWindowChecker.main() )
