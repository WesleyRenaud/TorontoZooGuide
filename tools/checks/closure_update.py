from __future__ import annotations

from datetime import date

from api.shared.date_values import DateValues
from .check_report import CheckReport


class ClosureUpdate():
   title: str
   description: str
   start: date
   end: date


   def __init__(
         self,
         title: str,
         description: str,
         start: date,
         end: date ) -> None:
      self.title = title
      self.description = description
      self.start = start
      self.end = end


   def line( self, detail: str ) -> str:
      return CheckReport.join_lines( [
         self.title,
         CheckReport.detail_item( detail ),
      ] )


   def added_line( self ) -> str:
      when = (
         DateValues.format_display_date_value( self.start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )
      return self.line( CheckReport.text( 'checks.setUpdateFrom' ) + when )


   def ended_line( self ) -> str:
      return self.line( CheckReport.text( 'checks.endedUpdate' ) )


   def extended_line( self ) -> str:
      when = (
         DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )
      return self.line( CheckReport.text( 'checks.extendedUpdateThrough' ) + when )
