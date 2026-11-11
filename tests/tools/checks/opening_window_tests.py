from __future__ import annotations

from datetime import date

import pytest

from api.shared.peak_months import PeakMonths
from tools.checks.opening_window import OpeningWindow
from tools.checks.weekday_window import WeekdayWindow


TODAY = date( 2026, 11, 9 )
DAILY = WeekdayWindow( frozenset( range( 7 ) ), False )
WEEKENDS = WeekdayWindow( frozenset( { 5, 6 } ), False )
OPEN_MONTHS = PeakMonths()
JUNE_THROUGH_OCTOBER = PeakMonths( 6, 10, 6, 10 )
WEEKDAY_AND_WEEKEND = PeakMonths( 6, 8, 6, 10 )


def _active( end: date | None, pattern: WeekdayWindow = DAILY ) -> OpeningWindow:
   return OpeningWindow( date( 2026, 1, 1 ), end, pattern )


def Test_Replacement_TestMatchingWindowPastTwoWeeks_ExpectNoEnd() -> None:
   active = _active( date( 2026, 12, 31 ) )

   replacement = OpeningWindow.replacement( DAILY, active, TODAY, OPEN_MONTHS )

   assert replacement == OpeningWindow( active.start, None, DAILY )


def Test_Replacement_TestOpenEndedWindow_ExpectNoChange() -> None:
   replacement = OpeningWindow.replacement( DAILY, _active( None ), TODAY, OPEN_MONTHS )

   assert replacement == None


def Test_Replacement_TestDifferentDays_ExpectNoEnd() -> None:
   replacement = OpeningWindow.replacement(
      WEEKENDS,
      _active( date( 2026, 12, 31 ) ),
      TODAY,
      OPEN_MONTHS,
   )

   assert replacement == OpeningWindow( TODAY, None, WEEKENDS )


def Test_Replacement_TestNoLocalWindow_ExpectNoEnd() -> None:
   replacement = OpeningWindow.replacement( DAILY, None, TODAY, OPEN_MONTHS )

   assert replacement == OpeningWindow( TODAY, None, DAILY )


def Test_Replacement_TestMatchingWindowEndingToday_ExpectNoEnd() -> None:
   active = _active( TODAY )

   replacement = OpeningWindow.replacement( DAILY, active, TODAY, OPEN_MONTHS )

   assert replacement == OpeningWindow( active.start, None, DAILY )


def Test_Replacement_TestMatchingWindowEndingTomorrow_ExpectNoEnd() -> None:
   active = _active( TODAY )

   replacement = OpeningWindow.replacement(
      DAILY,
      _active( date( 2026, 11, 10 ) ),
      TODAY,
      OPEN_MONTHS,
   )

   assert replacement == OpeningWindow( active.start, None, DAILY )


def Test_Replacement_TestMatchingWindowEndingInTwoWeeks_ExpectNoEnd() -> None:
   active = _active( date( 2026, 11, 23 ) )

   replacement = OpeningWindow.replacement( DAILY, active, TODAY, OPEN_MONTHS )

   assert replacement == OpeningWindow( active.start, None, DAILY )


@pytest.mark.parametrize(
   'today, current_end',
   [
      ( date( 2026, 10, 1 ), date( 2026, 10, 20 ) ),
      ( date( 2026, 10, 1 ), date( 2026, 10, 31 ) ),
      ( date( 2026, 10, 1 ), date( 2026, 11, 1 ) ),
      ( date( 2026, 10, 1 ), date( 2026, 10, 10 ) ),
      ( date( 2026, 10, 25 ), date( 2026, 10, 27 ) ),
      ( date( 2026, 10, 25 ), date( 2026, 10, 31 ) ),
      ( date( 2026, 11, 1 ), date( 2026, 11, 20 ) ),
      ( date( 2026, 11, 1 ), date( 2026, 12, 31 ) ),
      ( date( 2026, 11, 1 ), date( 2026, 11, 10 ) ),
      ( date( 2026, 11, 1 ), date( 2026, 11, 15 ) ),
   ],
)
def Test_Replacement_TestJuneThroughOctober_ExpectTargetEnd(
      today: date,
      current_end: date ) -> None:
   active = _active( current_end )
   target = JUNE_THROUGH_OCTOBER.schedule_end( DAILY.weekend_only(), today )

   replacement = OpeningWindow.replacement(
      DAILY,
      active,
      today,
      JUNE_THROUGH_OCTOBER,
   )

   if current_end == target:
      assert replacement == None
      return

   assert replacement == OpeningWindow( active.start, target, DAILY )


@pytest.mark.parametrize(
   'today, website, app, current_end',
   [
      ( date( 2026, 7, 1 ), DAILY, DAILY, date( 2026, 7, 10 ) ),
      ( date( 2026, 7, 1 ), DAILY, DAILY, date( 2026, 10, 31 ) ),
      ( date( 2026, 7, 1 ), DAILY, WEEKENDS, date( 2026, 7, 20 ) ),
      ( date( 2026, 7, 1 ), DAILY, WEEKENDS, date( 2026, 12, 31 ) ),
      ( date( 2026, 7, 1 ), WEEKENDS, DAILY, date( 2026, 7, 20 ) ),
      ( date( 2026, 7, 1 ), WEEKENDS, WEEKENDS, date( 2026, 7, 20 ) ),
      ( date( 2026, 8, 15 ), DAILY, DAILY, date( 2026, 10, 15 ) ),
      ( date( 2026, 8, 15 ), WEEKENDS, WEEKENDS, date( 2026, 8, 20 ) ),
      ( date( 2026, 9, 1 ), DAILY, DAILY, date( 2026, 9, 10 ) ),
      ( date( 2026, 9, 1 ), DAILY, DAILY, date( 2026, 10, 31 ) ),
      ( date( 2026, 9, 1 ), WEEKENDS, WEEKENDS, date( 2026, 9, 10 ) ),
      ( date( 2026, 9, 1 ), WEEKENDS, WEEKENDS, date( 2026, 11, 30 ) ),
      ( date( 2026, 11, 1 ), DAILY, DAILY, date( 2026, 12, 31 ) ),
      ( date( 2026, 11, 1 ), WEEKENDS, WEEKENDS, date( 2026, 11, 10 ) ),
   ],
)
def Test_Replacement_TestWeekdayAndWeekendWindows_ExpectWebsiteSchedule(
      today: date,
      website: WeekdayWindow,
      app: WeekdayWindow,
      current_end: date ) -> None:
   active = _active( current_end, app )
   target = WEEKDAY_AND_WEEKEND.schedule_end( website.weekend_only(), today )

   replacement = OpeningWindow.replacement(
      website,
      active,
      today,
      WEEKDAY_AND_WEEKEND,
   )

   if website.matches( app ):
      assert replacement == OpeningWindow( active.start, target, website )
      return

   assert replacement == OpeningWindow( today, target, website )
