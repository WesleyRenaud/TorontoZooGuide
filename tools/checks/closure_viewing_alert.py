from __future__ import annotations

from datetime import date

from .animal_catalogue import AnimalCatalogue
from .animal_detail_image import AnimalDetailImage
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from api.animals.status.animal_viewing_alert import AnimalViewingAlert
from api.app_string_provider import AppStringProvider
from api.models import Update
from api.shared.date_values import DateValues
from api.shared.text_values import TextValues
from api.updates.domain.update_type import UpdateType
from .check_report import CheckReport
from .exhibit_name import ExhibitName
from .paths import Paths
from .website_page import WebsitePage


class ClosureViewingAlert():
   species: str
   exhibit: str
   off_display: bool
   scope: str
   title: str
   description: str
   start: date
   end: date | None
   message: str
   replacing: bool


   def __init__(
         self,
         species: str,
         exhibit: str,
         off_display: bool,
         scope: str,
         title: str,
         description: str,
         start: date,
         end: date | None,
         replacing: bool ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.off_display = off_display
      self.scope = scope
      self.title = title
      self.description = description
      self.start = start
      self.end = end
      self.message = ''
      self.replacing = replacing


   def sort_key( self ) -> tuple[ str, str ]:
      return ( self.species.casefold(), self.exhibit.casefold() )


   def matches( self, stored: AnimalViewingAlert ) -> bool:
      return (
         stored.message == self.message
         and DateValues.parse_date_value( stored.start_date ) == self.start
         and DateValues.parse_date_value( stored.end_date ) == self.end
      )


   def needs_save( self, stored: list[ AnimalViewingAlert ] ) -> bool:
      for current in stored:
         if current.species == self.species and current.exhibit == self.exhibit:
            return not self.matches( current )

      return True


   @classmethod
   def detail_line(
         cls,
         species: str,
         exhibit: str,
         details: list[ str ] ) -> str:
      rows = [
         AppStringProvider.format(
            'format.middleDotPair',
            first=species,
            second=exhibit,
         ),
      ]
      photo = AnimalDetailImage.source( exhibit, species )

      if ( Paths.ROOT / photo ).is_file():
         rows.append( CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo ) )

      for detail in details:
         rows.append( CheckReport.detail_item( detail ) )

      return CheckReport.join_lines( rows )


   def line( self ) -> str:
      action = 'checks.updatedViewingAlert' if self.replacing else 'checks.setViewingAlert'
      return self.detail_line(
         self.species,
         self.exhibit,
         [
            CheckReport.text( action ),
            self.message,
         ],
      )


   @classmethod
   def removal_line( cls, alert: AnimalViewingAlert ) -> str:
      return cls.detail_line(
         alert.species,
         alert.exhibit,
         [
            CheckReport.text( 'checks.removedViewingAlert' ),
            alert.message,
         ],
      )


   @classmethod
   def without_closure(
         cls,
         stored: list[ AnimalViewingAlert ],
         chosen: list[ ClosureViewingAlert ],
         today: date ) -> list[ AnimalViewingAlert ]:
      kept = {
         ( alert.species, alert.exhibit )
         for alert in chosen
      }
      return [
         alert
         for alert in stored
         if ( alert.species, alert.exhibit ) not in kept
         and DateValues.is_date_in_range( today, alert.start_date, alert.end_date )
      ]


   @classmethod
   def names_species( cls, text: str, species: str ) -> bool:
      key = AnimalCatalogue.comparison_key( species, False )
      haystack = TextValues.spaced( WebsitePage.normalize_name( text ) )
      return (
         TextValues.spaced( key ) in haystack
         or TextValues.spaced( TextValues.plural( key ) ) in haystack
      )


   @classmethod
   def exhibits_for(
         cls,
         species: str,
         exhibits: list[ str ],
         off_display: list[ TemporaryOffDisplayAnimal ],
         today: date ) -> list[ str ]:
      current = [
         animal.exhibit
         for animal in off_display
         if animal.species == species and animal.covers( today )
      ]

      if len( current ) == 1:
         return current

      if len( exhibits ) == 1:
         return exhibits

      return []


   @classmethod
   def off_display_animal(
         cls,
         species: str,
         exhibit: str,
         off_display: list[ TemporaryOffDisplayAnimal ],
         today: date ) -> TemporaryOffDisplayAnimal | None:
      for animal in off_display:
         if (
            animal.species == species
            and animal.exhibit == exhibit
            and animal.covers( today )
         ):
            return animal

      return None


   @classmethod
   def closure_end( cls, update: Update ) -> date:
      if not update.end_date:
         return date.max

      return DateValues.parse_date_value( update.end_date ) or date.max


   @classmethod
   def window( cls, update: Update ) -> tuple[ date, date | None ] | None:
      if update.update_type != UpdateType.CLOSURE.value or not update.start_date:
         return None

      start = DateValues.parse_date_value( update.start_date )

      if start == None:
         return None

      end = DateValues.parse_date_value( update.end_date ) if update.end_date else None
      return ( start, end )


   @classmethod
   def matched(
         cls,
         text: str,
         placements: list[ AnimalSpeciesExhibit ],
         off_display: list[ TemporaryOffDisplayAnimal ],
         today: date ) -> list[ AnimalSpeciesExhibit ]:
      found = []

      for species in dict.fromkeys(
         placement.species
         for placement in placements
         if cls.names_species( text, placement.species )
      ):
         exhibits = [
            placement.exhibit
            for placement in placements
            if placement.species == species
         ]
         mentioned = ExhibitName.mentioned_in( text, exhibits )

         for exhibit in mentioned or cls.exhibits_for( species, exhibits, off_display, today ):
            found.append( AnimalSpeciesExhibit( species=species, exhibit=exhibit ) )

      return found


   @classmethod
   def for_animal(
         cls,
         update: Update,
         species: str,
         exhibit: str,
         start: date,
         end: date | None,
         off_display: list[ TemporaryOffDisplayAnimal ],
         today: date,
         replacing: bool ) -> ClosureViewingAlert:
      animal = cls.off_display_animal( species, exhibit, off_display, today )
      scope = ''

      if animal != None:
         scope = animal.viewing_scope or ''

      return cls(
         species,
         exhibit,
         animal != None,
         scope,
         update.title,
         update.description,
         start,
         end,
         replacing,
      )


   @classmethod
   def replace(
         cls,
         alerts: list[ ClosureViewingAlert ],
         alert: ClosureViewingAlert ) -> None:
      for index, existing in enumerate( alerts ):
         if existing.species == alert.species and existing.exhibit == alert.exhibit:
            alerts[ index ] = alert
            return

      alerts.append( alert )


   @classmethod
   def choose(
         cls,
         closures: list[ Update ],
         placements: list[ AnimalSpeciesExhibit ],
         off_display: list[ TemporaryOffDisplayAnimal ],
         stored: list[ AnimalViewingAlert ],
         today: date ) -> list[ ClosureViewingAlert ]:
      replacing = {
         AnimalSpeciesExhibit( species=alert.species, exhibit=alert.exhibit )
         for alert in stored
      }
      chosen: list[ ClosureViewingAlert ] = []

      for update in sorted(
         closures,
         key=lambda update: ( cls.closure_end( update ), update.title.casefold() ),
      ):
         window = cls.window( update )

         if window == None:
            continue

         start, end = window
         text = TextValues.beside( update.title, update.description )

         for place in cls.matched( text, placements, off_display, today ):
            cls.replace( chosen, cls.for_animal(
               update,
               place.species,
               place.exhibit,
               start,
               end,
               off_display,
               today,
               place in replacing,
            ) )

      return sorted( chosen, key=lambda alert: alert.sort_key() )
