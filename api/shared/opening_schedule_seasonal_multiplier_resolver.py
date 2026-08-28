from __future__ import annotations

from ..types import Types


class OpeningScheduleSeasonalMultiplierResolver():
   @classmethod
   def resolve(
         cls,
         *,
         weekday_multiplier: Types.SeasonalMultiplier,
         weekend_holiday_multiplier: Types.SeasonalMultiplier,
         is_weekend_or_holiday: bool ) -> Types.SeasonalMultiplier:
      if is_weekend_or_holiday:
         return weekend_holiday_multiplier

      return weekday_multiplier
