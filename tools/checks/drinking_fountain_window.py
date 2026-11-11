from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from api.drinking_fountains.domain.drinking_fountain_season import DrinkingFountainSeason
from api.drinking_fountains.domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from api.shared.date_values import DateValues
from .check_report import CheckReport


@dataclass( frozen=True )
class DrinkingFountainWindow():
   closed: bool
   start: date
   end: date


   @classmethod
   def replacement(
         cls,
         website_closed: bool,
         status: SeasonalDrinkingFountains,
         today: date ) -> DrinkingFountainWindow | None:
      target = DrinkingFountainSeason.end_for( website_closed, today )
      covers = DateValues.is_date_in_range( today, status.start, status.end )
      same_state = status.is_closed == website_closed

      if covers and same_state and status.end == target:
         return None

      if covers and same_state and status.start is not None:
         return cls( website_closed, status.start, target )

      return cls( website_closed, today, target )


   def detail( self ) -> str:
      key = 'checks.setClosedForSeasonFrom' if self.closed else 'checks.setOpenForSeasonFrom'
      when = (
         DateValues.format_display_date_value( self.start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )

      return CheckReport.detail_item( CheckReport.text( key ) + when )
