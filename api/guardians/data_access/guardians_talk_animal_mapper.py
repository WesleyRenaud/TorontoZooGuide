from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...types import Row


class GuardiansTalkAnimalMapper():
   @classmethod
   def map_linked_animal( cls, row: Row ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey.from_values(
         row[ 'SPECIES' ],
         row[ 'EXHIBIT' ] )


   @classmethod
   def map_linked_animals( cls, rows: list[ Row ] ) -> list[ SpeciesExhibitKey ]:
      return [
         cls.map_linked_animal( row )
         for row in rows
      ]
