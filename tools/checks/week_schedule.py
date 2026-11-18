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
      weekdays = { slot.weekday for slot in slots }
      scheduled = [
         day
         for day in dates
         if day.weekday() in weekdays
      ]

      if scheduled == []:
         return None

      return cls(
         start=min( scheduled ),
         end=max( scheduled ),
         slots=frozenset( slots ),
      )


   def matches( self, other: WeekSchedule | None ) -> bool:
      return other != None and self == other
