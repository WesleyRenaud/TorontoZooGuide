from __future__ import annotations

from ..data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from .seasonal_drinking_fountains import SeasonalDrinkingFountains
from ...shared.date_values import DateValues


class SeasonalDrinkingFountainsBuilder():
   @classmethod
   def build( cls, record: DrinkingFountainStatusRecord ) -> SeasonalDrinkingFountains:
      return SeasonalDrinkingFountains(
         is_closed=bool( record.is_closed ),
         start=DateValues.parse_date_value( record.start_date ),
         end=DateValues.parse_date_value( record.end_date ),
      )
