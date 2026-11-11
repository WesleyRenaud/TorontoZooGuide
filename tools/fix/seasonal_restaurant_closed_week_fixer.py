from __future__ import annotations

from datetime import date
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.domain.seasonal_restaurant import SeasonalRestaurant
from api.shared.date_values import DateValues
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.paths import Paths
from tools.checks.restaurant_detail_image import RestaurantDetailImage
from tools.checks.season_window import SeasonWindow


class SeasonalRestaurantClosedWeekFixer():
   @classmethod
   def extension_end( cls, restaurant: SeasonalRestaurant, today: date ) -> date:
      return SeasonWindow.week_extension_end( restaurant.end, today )


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
   def line( cls, name: str, end: date ) -> str:
      return cls.item(
         name,
         CheckReport.text( 'checks.extendedClosedForSeasonThrough' )
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
         restaurants = {
            restaurant.name: restaurant
            for restaurant in RestaurantCoordinator.get_seasonal_restaurants()
         }
         lines = []

         for name in names:
            restaurant = restaurants[ name ]
            start = today if restaurant.start == None else restaurant.start
            end = cls.extension_end( restaurant, today )
            RestaurantCoordinator.set_restaurant_as_closed_for_season(
               restaurant=name,
               start_date=start,
               end_date=end,
               message='',
            )
            lines.append( cls.line( name, end ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
