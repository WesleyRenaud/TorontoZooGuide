from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.date_values import DateValues


@dataclass( frozen=True )
class SeasonalRestaurant:
   name: str
   menu_link: str
   is_closed: bool
   start: date | None
   end: date | None
   closed_for_season: bool


   def closed_for_season_on( self, today: date ) -> bool:
      if not self.is_closed or not self.closed_for_season:
         return False

      return DateValues.is_date_in_range( today, self.start, self.end )
