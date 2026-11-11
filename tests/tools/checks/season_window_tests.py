from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import CalendarDates
from tools.checks.season_window import SeasonWindow


TODAY = date( 2027, 4, 30 )


def Test_NeedsWeekExtension_TestEndWithinAWeek_ExpectExtension() -> None:
   assert SeasonWindow.needs_week_extension( True, date( 2027, 5, 4 ), TODAY )


def Test_NeedsWeekExtension_TestEndInAWeek_ExpectNoExtension() -> None:
   horizon = CalendarDates.one_week_later( TODAY )

   assert SeasonWindow.needs_week_extension( True, horizon, TODAY ) is False


def Test_NeedsWeekExtension_TestAlreadyOpen_ExpectExtension() -> None:
   assert SeasonWindow.needs_week_extension( False, date( 2027, 4, 1 ), TODAY )


def Test_WeekExtensionEnd_TestEndWithinAWeek_ExpectWeekAfterTheNextDay() -> None:
   end = date( 2027, 5, 4 )

   assert SeasonWindow.week_extension_end( end, TODAY ) == date( 2027, 5, 12 )


def Test_WeekExtensionEnd_TestEndToday_ExpectWeekFromTomorrow() -> None:
   assert SeasonWindow.week_extension_end( TODAY, TODAY ) == date( 2027, 5, 8 )
