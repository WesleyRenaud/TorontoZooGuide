from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ...shared.name_matching_query import normalize_search_key


@dataclass( frozen=True )
class SpeciesExhibitKey:
   species: str
   exhibit: str

   def __post_init__( self ) -> None:
      object.__setattr__( self, 'species', normalize_search_key( self.species ) )
      object.__setattr__( self, 'exhibit', normalize_search_key( self.exhibit ) )


   @classmethod
   def from_values( cls, species: str | None, exhibit: str | None ) -> Self:
      return cls( species=species or '', exhibit=exhibit or '' )
