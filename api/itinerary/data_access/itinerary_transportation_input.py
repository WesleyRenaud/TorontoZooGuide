from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ...shared.value_conversion import ValueConversion


@dataclass( frozen=True )
class ItineraryTransportationInput:
   name: str
   added_as_attraction: bool

   @classmethod
   def from_wire( cls, wire: dict[ str, object ] ) -> Self:
      return cls(
         name=str( wire[ 'name' ] ),
         added_as_attraction=ValueConversion.as_boolean(
            wire[ 'added_as_attraction' ] ),
      )


   @classmethod
   def from_wires(
         cls,
         wires: list[ dict[ str, object ] ] | None,
      ) -> list[ Self ]:
      return [
         cls.from_wire( wire )
         for wire in wires or []
      ]
