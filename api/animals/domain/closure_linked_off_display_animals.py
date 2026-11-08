from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .animal_species_exhibit import AnimalSpeciesExhibit
from .closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal


@dataclass( frozen=True )
class ClosureLinkedOffDisplayAnimals:
   title: str
   start: date
   animals: list[ ClosureLinkedOffDisplayAnimal ]


   def ends_on( self, day: date ) -> bool:
      return any( animal.end == day for animal in self.animals )


   def enclosures( self ) -> list[ AnimalSpeciesExhibit ]:
      return list( dict.fromkeys(
         AnimalSpeciesExhibit( species=animal.species, exhibit=animal.exhibit )
         for animal in self.animals
      ) )


   @classmethod
   def groups(
         cls,
         animals: list[ ClosureLinkedOffDisplayAnimal ] ) -> list[ ClosureLinkedOffDisplayAnimals ]:
      grouped = {}

      for animal in animals:
         key = ( animal.closure_update_title, animal.closure_update_start )
         grouped.setdefault( key, [] ).append( animal )

      return [
         cls(
            title=title,
            start=start,
            animals=members,
         )
         for ( title, start ), members in grouped.items()
      ]
