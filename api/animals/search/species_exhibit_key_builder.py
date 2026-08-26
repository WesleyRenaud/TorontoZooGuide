from __future__ import annotations

from typing import Any

from ...models import Animal
from .species_exhibit_key import SpeciesExhibitKey


class SpeciesExhibitKeyBuilder():
   @classmethod
   def from_values(
         cls,
         species: str,
         exhibit: str ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey.from_values( species, exhibit )


   @classmethod
   def from_animal( cls, animal: Animal ) -> SpeciesExhibitKey:
      return cls.from_values( animal.species, animal.exhibit )


   @classmethod
   def from_animals( cls, animals: list[ Any ] ) -> list[ SpeciesExhibitKey ]:
      return [
         cls.from_values( animal.species, animal.exhibit )
         for animal in animals
      ]


   @classmethod
   def any_linked_in(
         cls,
         animal_keys: list[ SpeciesExhibitKey ],
         linked_animals: list[ SpeciesExhibitKey ] ) -> bool:
      return any(
         linked_animal in animal_keys
         for linked_animal in linked_animals
      )
