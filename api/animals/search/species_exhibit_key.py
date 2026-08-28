from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ...shared.text_values import TextValues


@dataclass( frozen=True )
class SpeciesExhibitKey:
   species: str
   exhibit: str

   def __post_init__( self ) -> None:
      object.__setattr__( self, 'species', TextValues.normalize_for_matching( self.species ) )
      object.__setattr__( self, 'exhibit', TextValues.normalize_for_matching( self.exhibit ) )


   @classmethod
   def from_values( cls, species: str | None, exhibit: str | None ) -> Self:
      return cls( species=species or '', exhibit=exhibit or '' )
