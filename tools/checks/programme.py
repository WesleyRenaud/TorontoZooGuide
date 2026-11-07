from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .programme_day import ProgrammeDay
from .programme_talk import ProgrammeTalk


@dataclass( frozen=True )
class Programme:
   dates: list[ date ]
   talks: list[ ProgrammeTalk ]


   @classmethod
   def from_days( cls, days: list[ ProgrammeDay ] ) -> Programme:
      return cls(
         dates=[ day.scheduled_date for day in days ],
         talks=[
            talk
            for day in days
            for talk in day.talks
         ],
      )
