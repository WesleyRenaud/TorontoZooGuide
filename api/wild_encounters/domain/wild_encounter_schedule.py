from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from datetime import timedelta


@dataclass( frozen=True )
class WildEncounterSchedule:
   name: str
   start: date | None
   end: date | None
   encounter_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool


   def covers( self, day: date ) -> bool:
      if self.start == None or self.start > day:
         return False

      return self.end == None or self.end > day


   def last_day( self ) -> date | None:
      if self.end == None:
         return None

      return self.end - timedelta( days=1 )


   @classmethod
   def dates(
         cls,
         schedules: list[ WildEncounterSchedule ],
         name: str,
         first: date,
         last: date ) -> list[ date ]:
      found: list[ date ] = []
      current = first

      while current <= last:
         weekday = current.weekday()

         for schedule in schedules:
            if schedule.name == name and schedule.covers( current ) and weekday in schedule.weekday_indexes():
               found.append( current )
               break

         current += timedelta( days=1 )

      return found


   def weekday_indexes( self ) -> set[ int ]:
      flags = (
         self.monday,
         self.tuesday,
         self.wednesday,
         self.thursday,
         self.friday,
         self.saturday,
         self.sunday,
      )
      return {
         index
         for index, flag in enumerate( flags )
         if flag
      }
