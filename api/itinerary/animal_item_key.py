from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ..shared.value_conversion import ValueConversion

ANIMAL_ITEM_KEY_SEPARATOR = '||'


@dataclass( frozen=True )
class AnimalScheduleItemKey:
   species: str
   exhibit: str
   enclosure_name: str | None = None

   @classmethod
   def from_wire( cls, wire: str ) -> Self | None:
      parts = [
         part.strip()
         for part in wire.split( ANIMAL_ITEM_KEY_SEPARATOR )
      ]

      if len( parts ) not in ( 2, 3 ):
         return None

      species = parts[ 0 ]
      exhibit = parts[ 1 ]

      if not species or not exhibit:
         return None

      enclosure_name = (
         ValueConversion.as_nullable_string( parts[ 2 ] )
         if len( parts ) == 3
         else None )

      return cls(
         species=species,
         exhibit=exhibit,
         enclosure_name=enclosure_name,
      )


   def to_wire( self ) -> str:
      base = (
         f'{ self.species.strip() }'
         f'{ ANIMAL_ITEM_KEY_SEPARATOR }'
         f'{ self.exhibit.strip() }' )

      if self.enclosure_name:
         return (
            f'{ base }'
            f'{ ANIMAL_ITEM_KEY_SEPARATOR }'
            f'{ self.enclosure_name.strip() }' )

      return base


   @classmethod
   def wire(
         cls,
         species: str,
         exhibit: str,
         enclosure_name: str | None = None ) -> str:
      return cls(
         species=species,
         exhibit=exhibit,
         enclosure_name=enclosure_name ).to_wire()


   @classmethod
   def parse_species_exhibit( cls, key: str ) -> tuple[ str, str ] | None:
      parsed = cls.from_wire( key )

      if parsed is None:
         return None

      return parsed.species, parsed.exhibit

