from __future__ import annotations

from api.shared.opening_schedule_seasonal_multiplier_resolver import OpeningScheduleSeasonalMultiplierResolver


WEEKDAY_MULTIPLIER = 0.8
WEEKEND_MULTIPLIER = 1.0


def Test_Resolve_TestWeekdayVisit_ExpectWeekdayMultiplier() -> None:
   multiplier = OpeningScheduleSeasonalMultiplierResolver.resolve(
      weekday_multiplier=WEEKDAY_MULTIPLIER,
      weekend_holiday_multiplier=WEEKEND_MULTIPLIER,
      is_weekend_or_holiday=False )

   assert multiplier == WEEKDAY_MULTIPLIER


def Test_Resolve_TestWeekendVisit_ExpectWeekendMultiplier() -> None:
   multiplier = OpeningScheduleSeasonalMultiplierResolver.resolve(
      weekday_multiplier=WEEKDAY_MULTIPLIER,
      weekend_holiday_multiplier=WEEKEND_MULTIPLIER,
      is_weekend_or_holiday=True )

   assert multiplier == WEEKEND_MULTIPLIER
