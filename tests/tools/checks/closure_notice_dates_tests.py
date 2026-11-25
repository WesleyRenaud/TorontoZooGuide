from __future__ import annotations

from datetime import date

from tools.checks.closure_notice_dates import ClosureNoticeDates


def Test_Parse_TestMidMonthAcrossNewYear_ExpectOriginalStartAndRollingEnd() -> None:
   text = 'December 28 – mid-January'

   assert ClosureNoticeDates.parse( text, date( 2026, 12, 24 ) ) == ClosureNoticeDates(
      start=date( 2026, 12, 28 ),
      end=date( 2027, 1, 15 ),
   )
   assert ClosureNoticeDates.parse( text, date( 2027, 1, 12 ) ) == ClosureNoticeDates(
      start=date( 2026, 12, 28 ),
      end=date( 2027, 1, 19 ),
   )


def Test_Parse_TestFirmReopeningDateAfterEstimate_ExpectFirmDate() -> None:
   text = 'Closed until mid-December. The exhibit reopens on December 12.'

   assert ClosureNoticeDates.parse( text, date( 2026, 12, 10 ) ) == ClosureNoticeDates(
      date( 2026, 12, 12 ),
      date( 2026, 12, 12 ),
   )


def Test_Parse_TestMidMonthWithYearAndNoStart_ExpectEndOnly() -> None:
   assert ClosureNoticeDates.parse(
      'Closed through mid-January 2027.',
      date( 2026, 12, 24 ),
   ) == ClosureNoticeDates( end=date( 2027, 1, 15 ) )


def Test_Parse_TestMidFebruaryWithoutYear_ExpectYearFromRunDate() -> None:
   assert ClosureNoticeDates.parse(
      'Closed through mid-February.',
      date( 2027, 1, 28 ),
   ) == ClosureNoticeDates( end=date( 2027, 2, 15 ) )


def Test_Parse_TestMidMonthWithoutYearAroundNewYear_ExpectNearbyMidpoint() -> None:
   assert ClosureNoticeDates.parse(
      'Closed through mid-January.',
      date( 2026, 12, 28 ),
   ) == ClosureNoticeDates( end=date( 2027, 1, 15 ) )
   assert ClosureNoticeDates.parse(
      'Closed through mid-December.',
      date( 2027, 1, 2 ),
   ) == ClosureNoticeDates( end=date( 2027, 1, 9 ) )


def Test_Parse_TestUndatedNotice_ExpectNoDates() -> None:
   assert ClosureNoticeDates.parse( 'Closed for maintenance.', date( 2026, 11, 25 ) ) == ClosureNoticeDates()
