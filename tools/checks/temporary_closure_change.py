from __future__ import annotations

from datetime import date

from api.shared.date_values import DateValues
from api.shared.enums.item_type import ItemType
from .check_report import CheckReport


class TemporaryClosureChange():
   place: str
   message: str
   kind: ItemType
   start: date | None
   end: date | None
   photo_path: str


   def __init__(
         self,
         place: str,
         message: str,
         kind: ItemType,
         start: date | None,
         end: date | None,
         photo_path: str ) -> None:
      self.place = place
      self.message = message
      self.kind = kind
      self.start = start
      self.end = end
      self.photo_path = photo_path


   def photo_line( self ) -> str:
      return CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + self.photo_path )


   def line( self, detail: str ) -> str:
      return CheckReport.join_lines( [
         self.place,
         self.photo_line(),
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
      return self.line( CheckReport.text( 'checks.setTemporaryClosureFrom' ) + self.span() )


   def ended_line( self ) -> str:
      return self.line( CheckReport.text( 'checks.openedTemporaryClosure' ) )


   def extended_line( self ) -> str:
      when = (
         DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )
      return self.line(
         CheckReport.text( 'checks.extendedTemporaryClosureThrough' ) + when
      )
