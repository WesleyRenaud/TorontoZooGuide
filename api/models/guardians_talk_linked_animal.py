from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkLinkedAnimal:
   species: str
   exhibit: str

   def to_dict( self ) -> dict[ str, str ]:
      return {
         'species': self.species,
         'exhibit': self.exhibit,
      }
