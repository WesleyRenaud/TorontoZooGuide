from __future__ import annotations

from datetime import date
from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from tools.checks.attraction_detail_image import AttractionDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors


class SeasonalAttractionClosedFixer():
   @classmethod
   def line( cls, name: str, start: date, end: date ) -> str:
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
            CheckReport.text( 'checks.setClosedForSeasonFrom' )
            + DateValues.format_display_date_value( start )
            + CheckReport.text( 'checks.dateThrough' )
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
         lines = []

         for name in names:
            until_month = AttractionCoordinator.closed_for_season_until_month( name )
            end = CalendarDates.next_month_end( until_month, today )
            AttractionCoordinator.set_attraction_as_closed_for_season_until( name, today )
            lines.append( cls.line( name, today, end ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
