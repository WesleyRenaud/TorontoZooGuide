from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from .schedule_item_key_separator import ScheduleItemKeySeparator


@dataclass( frozen=True )
class TransportationScheduleItemKey:
   name: str
   added_as_attraction: bool

   @classmethod
   def from_wire( cls, wire: str ) -> Self | None:
      parts = wire.split( ScheduleItemKeySeparator.VALUE, 1 )

      if len( parts ) != 2:
         return None

      name = parts[ 0 ].strip()
      added_as_attraction_wire = parts[ 1 ].strip()

      if not name:
         return None

      if added_as_attraction_wire == '1':
         added_as_attraction = True
      elif added_as_attraction_wire == '0':
         added_as_attraction = False
      else:
         return None

      return cls(
         name=name,
         added_as_attraction=added_as_attraction )


   def to_wire( self ) -> str:
      return (
         f'{ self.name.strip() }'
         f'{ ScheduleItemKeySeparator.VALUE }'
         f'{ "1" if self.added_as_attraction else "0" }'
      )
