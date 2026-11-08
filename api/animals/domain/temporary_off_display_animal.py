from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .animal_species_exhibit import AnimalSpeciesExhibit
from .animal_viewing_scope import AnimalViewingScope
from ...shared.date_values import DateValues


@dataclass( frozen=True )
class TemporaryOffDisplayAnimal:
   species: str
   exhibit: str
   viewing_scope: str
   start: date | None
   end: date | None
   closure_update_title: str | None
   closure_update_start: date | None


   def covers( self, day: date ) -> bool:
      return DateValues.is_date_in_range( day, self.start, self.end )


   def enclosure( self ) -> AnimalSpeciesExhibit:
      return AnimalSpeciesExhibit( species=self.species, exhibit=self.exhibit )


   def scope( self ) -> AnimalViewingScope:
      return AnimalViewingScope.from_enclosure_name( self.viewing_scope )


   def shares_closure( self, other: TemporaryOffDisplayAnimal ) -> bool:
      return (
         self.closure_update_title != None
         and self.closure_update_title == other.closure_update_title
         and self.closure_update_start == other.closure_update_start
         and self.enclosure() != other.enclosure()
      )
