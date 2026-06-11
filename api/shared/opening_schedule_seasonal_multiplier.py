from __future__ import annotations

from ..types import SeasonalMultiplier


def get_day_seasonal_availability_multiplier(
      *,
      weekday_multiplier: SeasonalMultiplier,
      weekend_holiday_multiplier: SeasonalMultiplier,
      is_weekend_or_holiday: bool ) -> SeasonalMultiplier:
   if is_weekend_or_holiday:
      return weekend_holiday_multiplier

   return weekday_multiplier
