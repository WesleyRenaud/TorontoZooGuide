from __future__ import annotations

from datetime import date
from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.seasonal_attraction import SeasonalAttraction
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from tools.checks.attraction_detail_image import AttractionDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.season_window import SeasonWindow


class SeasonalAttractionClosedWeekFixer():
   @classmethod
   def extension_end( cls, attraction: SeasonalAttraction, today: date ) -> date:
      return SeasonWindow.week_extension_end( attraction.end, today )


   @classmethod
   def line( cls, name: str, end: date ) -> str:
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
         CheckReport.detail_item(
            CheckReport.text( 'checks.extendedClosedForSeasonThrough' )
            + DateValues.format_display_date_value( end )
            + CheckReport.text( 'checks.period' )
         ),
      ] )


   @classmethod
   def fix( cls, database: Path, today: date, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         attractions = {
            attraction.name: attraction
            for attraction in AttractionCoordinator.get_seasonal_attractions()
         }
         lines = []

         for name in names:
            attraction = attractions[ name ]
            start = today if attraction.start == None else attraction.start
            end = cls.extension_end( attraction, today )
            AttractionCoordinator.set_attraction_as_closed_for_season(
               attraction=name,
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
