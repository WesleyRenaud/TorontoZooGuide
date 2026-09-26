from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ...shared.calendar_dates import DateValues
from ...types import Types


@dataclass( frozen=True )
class VisitWindowOverflowKeepItem:
   name: str
   item_type: str
   start_time: Types.ScheduleTimeKey = None


   @classmethod
   def from_wire( cls, wire: dict[ str, object ] ) -> Self:
      return cls(
         name=str( wire[ 'name' ] ),
         item_type=str( wire[ 'item_type' ] ),
         start_time=DateValues.normalize_itinerary_schedule_time(
            wire.get( 'start_time' ) ) )


   @classmethod
   def from_wires(
         cls,
         wires: list[ dict[ str, object ] ] | None ) -> list[ Self ]:
      return [
         cls.from_wire( wire )
         for wire in wires or []
      ]
