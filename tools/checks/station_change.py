from __future__ import annotations

from datetime import date

from api.shared.date_values import DateValues
from .check_report import CheckReport


class StationChange():
   station: str
   message: str
   start: date
   end: date | None


   def __init__(
         self,
         station: str,
         message: str,
         start: date,
         end: date | None ) -> None:
      self.station = station
      self.message = message
      self.start = start
      self.end = end


   def line( self, detail: str ) -> str:
      return CheckReport.join_lines( [
         self.station,
         CheckReport.detail_item( self.message ),
         CheckReport.detail_item( detail ),
      ] )


   def span( self ) -> str:
      return (
         DateValues.format_display_date_value( self.start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )


   def added_line( self ) -> str:
      return self.line( CheckReport.text( 'checks.setStationFrom' ) + self.span() )


   def ended_line( self ) -> str:
      return self.line( CheckReport.text( 'checks.openedStation' ) )


   def extended_line( self ) -> str:
      when = (
         DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )
      return self.line( CheckReport.text( 'checks.extendedStationThrough' ) + when )
