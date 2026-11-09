from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .schedule_slot import ScheduleSlot


@dataclass( frozen=True )
class WeekSchedule:
   start: date
   end: date
   slots: frozenset[ ScheduleSlot ]


   @classmethod
   def build(
         cls,
         dates: list[ date ],
         slots: set[ ScheduleSlot ] ) -> WeekSchedule | None:
      if dates == [] or slots == set():
         return None

      return cls(
         start=min( dates ),
         end=max( dates ),
         slots=frozenset( slots ),
      )


   def matches( self, other: WeekSchedule | None ) -> bool:
      return other != None and self == other
