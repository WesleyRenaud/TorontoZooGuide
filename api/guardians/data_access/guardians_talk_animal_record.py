from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.animals_matching_query import viewing_spot_key_from_values
from ...animals.search.species_exhibit_key import SpeciesExhibitKey


@dataclass( frozen=True )
class GuardiansTalkAnimalRecord:
   talk_name: str
   location: str
   species: str
   exhibit: str
   enclosure_name: str | None = None


   def species_exhibit_key( self ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey.from_values( self.species, self.exhibit )


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return viewing_spot_key_from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )
