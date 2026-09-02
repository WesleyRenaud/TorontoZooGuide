from __future__ import annotations

from datetime import date

from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput


SAVE_INPUT = ItinerarySaveInput(
   date=date( 2026, 6, 15 ),
   arrival_time='09:30',
   departure_time='17:00',
)


def Test_Month_TestSaveInput_ExpectJune() -> None:
   assert SAVE_INPUT.month() == 6


def Test_Day_TestSaveInput_ExpectFifteenth() -> None:
   assert SAVE_INPUT.day() == 15


def Test_Year_TestSaveInput_ExpectTwentyTwentySix() -> None:
   assert SAVE_INPUT.year() == 2026
