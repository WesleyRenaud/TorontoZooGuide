from __future__ import annotations

from datetime import date

from api.drinking_fountains.data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from api.drinking_fountains.domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from api.drinking_fountains.domain.seasonal_drinking_fountains_builder import SeasonalDrinkingFountainsBuilder


def Test_Build_TestOpenEndedStatus_ExpectSeasonalDrinkingFountains() -> None:
   status = SeasonalDrinkingFountainsBuilder.build(
      DrinkingFountainStatusRecord(
         is_closed=True,
         start_date='2026-11-02',
         end_date=None,
         closed_message=None,
      )
   )

   assert status == SeasonalDrinkingFountains(
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
   )


def Test_Build_TestMissingDates_ExpectOpenRange() -> None:
   status = SeasonalDrinkingFountainsBuilder.build(
      DrinkingFountainStatusRecord(
         is_closed=True,
         start_date=None,
         end_date=None,
         closed_message=None,
      )
   )

   assert status.closed_for_season_on( date( 2026, 11, 2 ) ) is True


def Test_ClosedForSeasonOn_TestEndedStatus_ExpectNotClosed() -> None:
   status = SeasonalDrinkingFountains(
      is_closed=True,
      start=None,
      end=date( 2026, 5, 1 ),
   )

   assert status.closed_for_season_on( date( 2026, 11, 2 ) ) is False


def Test_ClosedForSeasonOn_TestOpenStatus_ExpectNotClosed() -> None:
   status = SeasonalDrinkingFountains(
      is_closed=False,
      start=date( 2026, 6, 1 ),
      end=date( 2026, 10, 31 ),
   )

   assert status.closed_for_season_on( date( 2026, 6, 15 ) ) is False
