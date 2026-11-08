from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.date_values import DateValues


@dataclass( frozen=True )
class EnclosureOffDisplayStatus:
   species: str
   exhibit: str
   start: date | None
   end: date | None


   def covers( self, day: date ) -> bool:
      return DateValues.is_date_in_range( day, self.start, self.end )
