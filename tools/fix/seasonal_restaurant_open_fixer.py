from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.paths import Paths
from tools.checks.restaurant_detail_image import RestaurantDetailImage


class SeasonalRestaurantOpenFixer():
   @classmethod
   def line( cls, name: str ) -> str:
      lines = [ ExhibitRegionColors.restaurant_label( name ) ]
      photo = RestaurantDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append(
            CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )
         )

      lines.append( CheckReport.detail_item( CheckReport.text( 'checks.setOpenForSeason' ) ) )
      return CheckReport.join_lines( lines )


   @classmethod
   def fix( cls, database: Path, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for name in names:
            RestaurantCoordinator.set_restaurant_as_open_for_season( name )
            lines.append( cls.line( name ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
