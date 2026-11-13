from __future__ import annotations

from datetime import date

from .animal_detail_image import AnimalDetailImage
from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .check_report import CheckReport
from .paths import Paths


class ViewingHours():
   species: str
   exhibit: str
   start: date | None
   end: date | None
   opens: str
   closes: str
   subject: str


   def __init__(
         self,
         species: str,
         exhibit: str,
         start: date | None,
         end: date | None,
         opens: str,
         closes: str,
         subject: str = '' ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.start = start
      self.end = end
      self.opens = opens
      self.closes = closes
      self.subject = subject if subject != '' else species


   def sort_key( self ) -> tuple[ str, str ]:
      return ( self.species.casefold(), self.exhibit.casefold() )


   def label( self ) -> str:
      return AppStringProvider.format(
         'format.middleDotPair',
         first=self.species,
         second=self.exhibit,
      )


   def photo_line( self ) -> str | None:
      photo = AnimalDetailImage.source( self.exhibit, self.species )

      if not ( Paths.ROOT / photo ).is_file():
         return None

      return CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )


   def line( self, detail: str, message: str = '' ) -> str:
      rows = [ self.label() ]
      photo = self.photo_line()

      if photo != None:
         rows.append( photo )

      rows.append( CheckReport.detail_item( detail ) )

      if message != '':
         rows.append( CheckReport.detail_item( message ) )

      return CheckReport.join_lines( rows )


   def guest_message( self ) -> str:
      if self.end == None:
         return ''

      return AppStringProvider.format(
         'guestStatus.animals.limitedViewingScheduleUntil',
         species=self.subject,
         dailyStartTime=self.opens,
         dailyEndTime=self.closes,
         endDate=DateValues.format_display_date_value( self.end ),
      )


   def scheduled_line( self ) -> str:
      return self.line(
         CheckReport.text( 'checks.setViewingHoursFrom' ),
         self.guest_message(),
      )


   def removed_line( self ) -> str:
      return self.line( CheckReport.text( 'checks.removedViewingHours' ) )


   def extended_line( self ) -> str:
      return self.line(
         CheckReport.text( 'checks.extendedViewingHoursThrough' ),
         self.guest_message(),
      )


   def trimmed_line( self ) -> str:
      return self.line(
         CheckReport.text( 'checks.trimmedViewingHoursThrough' ),
         self.guest_message(),
      )
