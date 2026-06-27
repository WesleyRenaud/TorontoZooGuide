from __future__ import annotations

from dataclasses import dataclass
from typing import Self

ANIMAL_ITEM_KEY_SEPARATOR = '||'


@dataclass( frozen=True )
class AnimalScheduleItemKey:
   species: str
   exhibit: str

   @classmethod
   def from_wire( cls, wire: str ) -> Self | None:
      parts = wire.split( ANIMAL_ITEM_KEY_SEPARATOR, 1 )

      if len( parts ) != 2:
         return None

      species = parts[ 0 ].strip()
      exhibit = parts[ 1 ].strip()

      if not species or not exhibit:
         return None

      return cls( species=species, exhibit=exhibit )


   def to_wire( self ) -> str:
      return (
         f'{ self.species.strip() }'
         f'{ ANIMAL_ITEM_KEY_SEPARATOR }'
         f'{ self.exhibit.strip() }' )


def format_animal_schedule_item_key( species: str, exhibit: str ) -> str:
   return AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit ).to_wire()


def parse_animal_schedule_item_key( key: str ) -> tuple[ str, str ] | None:
   parsed = AnimalScheduleItemKey.from_wire( key )

   if parsed is None:
      return None

   return parsed.species, parsed.exhibit
