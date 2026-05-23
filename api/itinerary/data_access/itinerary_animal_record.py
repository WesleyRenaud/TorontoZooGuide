from __future__ import annotations

from dataclasses import dataclass

from ...animals.logic.animals_matching_query import species_exhibit_key_from_values


@dataclass( frozen=True )
class ItineraryAnimalRecord:
   species: str
   exhibit: str
   old_likelihood: int | None
   new_likelihood: int | None


   def species_exhibit_key( self ) -> tuple[ str, str ]:
      return species_exhibit_key_from_values( self.species, self.exhibit )
