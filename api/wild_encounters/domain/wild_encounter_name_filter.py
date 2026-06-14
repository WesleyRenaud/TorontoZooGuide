from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterNameFilter:
   name: str


   def __post_init__( self ) -> None:
      object.__setattr__(
         self,
         'name',
         ( self.name or '' ).strip().lower() )


   def should_return_empty( self ) -> bool:
      return not self.name


   def allows_wild_encounter_name( self, name: str | None ) -> bool:
      return ( name or '' ).strip().lower() == self.name
