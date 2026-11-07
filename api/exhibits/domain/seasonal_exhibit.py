from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.date_values import DateValues


@dataclass( frozen=True )
class SeasonalExhibit:
   name: str
   is_closed: bool
   start: date | None
   end: date | None
   closed_for_season: bool


   @classmethod
   def lookup( cls, name: str, exhibits: list[ SeasonalExhibit ] ) -> SeasonalExhibit | None:
      return {
         exhibit.name.casefold(): exhibit
         for exhibit in exhibits
      }.get( name.casefold() )


   def closed_for_season_on( self, today: date ) -> bool:
      if not self.is_closed or not self.closed_for_season or self.start == None:
         return False

      return DateValues.is_date_in_range( today, self.start, self.end )
