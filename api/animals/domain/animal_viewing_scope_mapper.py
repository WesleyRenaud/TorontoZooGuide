from __future__ import annotations

from .animal_viewing_scope import AnimalViewingScope


class AnimalViewingScopeMapper():
   @classmethod
   def map_payload( cls, values: list[ str ] ) -> list[ AnimalViewingScope ]:
      return [
         AnimalViewingScope.from_enclosure_name( value )
         for value in values
      ]
