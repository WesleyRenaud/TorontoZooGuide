from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder


@dataclass( frozen=True )
class AttractionAnimalRecord:
   attraction: str
   species: str
   exhibit: str
   enclosure_name: str | None = None


   def species_exhibit_key( self ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey.from_values( self.species, self.exhibit )


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return ViewingSpotKeyBuilder.from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )
