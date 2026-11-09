from __future__ import annotations

from datetime import date
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.paths import Paths
from tools.checks.restaurant_detail_image import RestaurantDetailImage


class SeasonalRestaurantClosedUntilMonthFixer():
   @classmethod
   def item( cls, name: str, detail: str ) -> str:
      lines = [ ExhibitRegionColors.restaurant_label( name ) ]
      photo = RestaurantDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append(
            CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )
         )

      lines.append( CheckReport.detail_item( detail ) )
      return CheckReport.join_lines( lines )


   @classmethod
   def line( cls, name: str, start: date, end: date ) -> str:
      return cls.item(
         name,
         CheckReport.text( 'checks.setClosedForSeasonFrom' )
         + DateValues.format_display_date_value( start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( end )
         + CheckReport.text( 'checks.period' ),
      )


   @classmethod
   def fix( cls, database: Path, today: date, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for name in names:
            until_month = RestaurantCoordinator.closed_for_season_until_month( name )
            end = CalendarDates.next_month_end( until_month, today )
            RestaurantCoordinator.set_restaurant_as_closed_for_season_until( name, today )
            lines.append( cls.line( name, today, end ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
