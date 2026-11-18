from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass( frozen=True )
class DateSpan:
   start: date
   end: date | None


   def is_next_day( self, day: date ) -> bool:
      if self.end == None:
         return False

      return day == self.end + timedelta( days=1 )


   def extended_to( self, day: date ) -> DateSpan:
      return DateSpan( start=self.start, end=day )
