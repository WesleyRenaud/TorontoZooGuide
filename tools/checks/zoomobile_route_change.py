from __future__ import annotations

from datetime import date

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from api.shared.enums.transportation_name import TransportationName
from api.shared.text_values import TextValues
from .attraction_detail_image import AttractionDetailImage
from .check_report import CheckReport
from .paths import Paths


class ZoomobileRouteChange():
   route: str
   start: date
   end: date


   def __init__( self, route: str, start: date, end: date ) -> None:
      self.route = route
      self.start = start
      self.end = end


   def detail( self ) -> str:
      label = AppStringProvider.format( f'schedule.routeLabels.{ self.route }' )
      when = DateValues.format_display_date_value( self.end )
      route = TextValues.beside( label, CheckReport.text( 'checks.routeUntil' ) )
      return (
         CheckReport.text( 'checks.setRouteTo' )
         + TextValues.beside( route, when )
         + CheckReport.text( 'checks.period' )
      )


   def line( self ) -> str:
      rows = [ TransportationName.ZOOMOBILE.value ]
      photo = AttractionDetailImage.source( TransportationName.ZOOMOBILE.value )

      if ( Paths.ROOT / photo ).is_file():
         rows.append( CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo ) )

      rows.append( CheckReport.detail_item( self.detail() ) )
      return CheckReport.join_lines( rows )
