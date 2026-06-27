from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass( frozen=True )
class GuardiansTalkScheduleItemKey:
   name: str

   @classmethod
   def from_wire( cls, wire: str ) -> Self | None:
      name = wire.strip()

      if not name:
         return None

      return cls( name=name )


   def to_wire( self ) -> str:
      return self.name.strip()
