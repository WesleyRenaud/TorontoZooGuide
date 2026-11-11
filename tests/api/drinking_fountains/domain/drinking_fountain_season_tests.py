from __future__ import annotations

from datetime import date

from api.drinking_fountains.domain.drinking_fountain_season import DrinkingFountainSeason
from api.shared.calendar_dates import CalendarDates


NOVEMBER = date( 2026, 11, 11 )
FEBRUARY = date( 2026, 2, 10 )
APRIL = date( 2026, 4, 20 )
MARCH = date( 2026, 3, 15 )
JUNE = date( 2026, 6, 1 )
OCTOBER = date( 2026, 10, 20 )



def Test_ClosedEnd_TestNovember_ExpectNextApril30() -> None:
   end = DrinkingFountainSeason.closed_end( NOVEMBER )

   assert end == date( 2027, 4, 30 )


def Test_ClosedEnd_TestFebruary_ExpectThisApril30() -> None:
   end = DrinkingFountainSeason.closed_end( FEBRUARY )

   assert end == date( 2026, 4, 30 )


def Test_ClosedEnd_TestLateApril_ExpectApril30() -> None:
   end = DrinkingFountainSeason.closed_end( APRIL )

   assert end == date( 2026, 4, 30 )


def Test_ClosedEnd_TestJune_ExpectTwoWeeks() -> None:
   end = DrinkingFountainSeason.closed_end( JUNE )

   assert end == CalendarDates.two_weeks_later( JUNE )


def Test_OpenEnd_TestJune_ExpectOctober31() -> None:
   end = DrinkingFountainSeason.open_end( JUNE )

   assert end == date( 2026, 10, 31 )


def Test_OpenEnd_TestLateOctober_ExpectOctober31() -> None:
   end = DrinkingFountainSeason.open_end( OCTOBER )

   assert end == date( 2026, 10, 31 )


def Test_OpenEnd_TestNovember_ExpectTwoWeeks() -> None:
   end = DrinkingFountainSeason.open_end( NOVEMBER )

   assert end == CalendarDates.two_weeks_later( NOVEMBER )


def Test_OpenEnd_TestMarch_ExpectTwoWeeks() -> None:
   end = DrinkingFountainSeason.open_end( MARCH )

   assert end == CalendarDates.two_weeks_later( MARCH )
