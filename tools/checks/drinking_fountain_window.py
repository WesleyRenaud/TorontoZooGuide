from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from api.drinking_fountains.domain.drinking_fountain_season import DrinkingFountainSeason
from api.drinking_fountains.domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from api.shared.date_values import DateValues
from .check_report import CheckReport
from .opening_window import OpeningWindow
from .window_change import WindowChange


@dataclass( frozen=True )
class DrinkingFountainWindow():
   closed: bool
   start: date
   end: date
   change: WindowChange = WindowChange.SET


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
         start = status.start if status.start >= today else today
         return cls(
            website_closed,
            start,
            target,
            OpeningWindow.end_change( status.end, target ),
         )

      return cls( website_closed, today, target )


   def detail( self ) -> str:
      if self.change == WindowChange.EXTENDED:
         key = (
            'checks.extendedClosedForSeasonThrough'
            if self.closed
            else 'checks.extendedOpenForSeasonThrough'
         )
      elif self.change == WindowChange.TRIMMED:
         key = (
            'checks.trimmedClosedForSeasonThrough'
            if self.closed
            else 'checks.trimmedOpenForSeasonThrough'
         )
      else:
         key = 'checks.setClosedForSeasonFrom' if self.closed else 'checks.setOpenForSeasonFrom'

      if self.change == WindowChange.SET:
         when = (
            DateValues.format_display_date_value( self.start )
            + CheckReport.text( 'checks.dateThrough' )
            + DateValues.format_display_date_value( self.end )
            + CheckReport.text( 'checks.period' )
         )
      else:
         when = (
            DateValues.format_display_date_value( self.end )
            + CheckReport.text( 'checks.period' )
         )

      return CheckReport.detail_item( CheckReport.text( key ) + when )
