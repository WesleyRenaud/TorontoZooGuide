from __future__ import annotations

from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.attraction_detail_image import AttractionDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors


class SeasonalAttractionOpenFixer():
   @classmethod
   def line( cls, name: str ) -> str:
      return CheckReport.join_lines( [
         AppStringProvider.format(
            'format.middleDotPair',
            first=name,
            second=ExhibitRegionColors.attraction_region( name ),
         ),
         CheckReport.detail_item(
            CheckReport.text( 'checks.photo' )
            + AttractionDetailImage.source( name )
         ),
         CheckReport.detail_item( CheckReport.text( 'checks.setOpenForSeason' ) ),
      ] )


   @classmethod
   def fix( cls, database: Path, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for name in names:
            AttractionCoordinator.set_attraction_as_open_for_season( name )
            lines.append( cls.line( name ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
