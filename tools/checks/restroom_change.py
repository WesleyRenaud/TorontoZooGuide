from __future__ import annotations

from datetime import date

from api.shared.date_values import DateValues
from .check_report import CheckReport


class RestroomChange():
   restroom: str
   message: str
   closure: bool
   start: date | None
   end: date | None


   def __init__(
         self,
         restroom: str,
         message: str,
         closure: bool,
         start: date | None,
         end: date | None ) -> None:
      self.restroom = restroom
      self.message = message
      self.closure = closure
      self.start = start
      self.end = end


   def line( self, detail: str ) -> str:
      return CheckReport.join_lines( [
         self.restroom,
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
      key = 'checks.setRestroomFrom' if self.closure else 'checks.setRestroomAlertFrom'
      return self.line( CheckReport.text( key ) + self.span() )


   def ended_line( self ) -> str:
      key = 'checks.openedRestroom' if self.closure else 'checks.removedRestroomAlert'
      return self.line( CheckReport.text( key ) )


   def extended_line( self ) -> str:
      when = (
         DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )
      key = (
         'checks.extendedRestroomThrough'
         if self.closure
         else 'checks.extendedRestroomAlertThrough'
      )
      return self.line( CheckReport.text( key ) + when )
