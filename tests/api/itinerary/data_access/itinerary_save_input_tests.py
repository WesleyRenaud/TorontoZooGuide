from __future__ import annotations

from datetime import date

from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput


def Test_Month_TestSaveInput_ExpectJune() -> None:
   visit_date = date( 2026, 6, 15 )
   save_input = ItinerarySaveInput(
      date=visit_date,
      arrival_time='09:30',
      departure_time='17:00' )

   month = save_input.month()

   assert month == visit_date.month


def Test_Day_TestSaveInput_ExpectFifteenth() -> None:
   visit_date = date( 2026, 6, 15 )
   save_input = ItinerarySaveInput(
      date=visit_date,
      arrival_time='09:30',
      departure_time='17:00' )

   day = save_input.day()

   assert day == visit_date.day


def Test_Year_TestSaveInput_ExpectTwentyTwentySix() -> None:
   visit_date = date( 2026, 6, 15 )
   save_input = ItinerarySaveInput(
      date=visit_date,
      arrival_time='09:30',
      departure_time='17:00' )

   year = save_input.year()

   assert year == visit_date.year
