from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.date_values import DateValues


@dataclass( frozen=True )
class SeasonalOffDisplayAnimal:
   name: str
   is_off_display: bool
   start: date | None
   end: date | None
   off_for_season: bool


   @classmethod
   def species_name( cls, name: str, animals: list[ SeasonalOffDisplayAnimal ] ) -> str:
      folded = name.casefold()

      for animal in animals:
         if animal.name.casefold() == folded:
            return animal.name

      return name


   def off_for_season_on( self, today: date ) -> bool:
      if not self.is_off_display or not self.off_for_season:
         return False

      return DateValues.is_date_in_range( today, self.start, self.end )
