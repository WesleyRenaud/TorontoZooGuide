from __future__ import annotations

from datetime import date

from api.exhibits.domain.exhibit_season import ExhibitSeason


CANADIAN = ExhibitSeason( 4, 11 )
MAYAN = ExhibitSeason( 4, 10 )
KIDS = ExhibitSeason( 5, 10 )
NOVEMBER = date( 2026, 11, 11 )


def Test_EndFor_TestCanadianOpenInNovember_ExpectNovember30() -> None:
   assert CANADIAN.end_for( False, NOVEMBER ) == date( 2026, 11, 30 )


def Test_EndFor_TestMayanClosedInNovember_ExpectMarch31() -> None:
   assert MAYAN.end_for( True, NOVEMBER ) == date( 2027, 3, 31 )


def Test_EndFor_TestKidsClosedInNovember_ExpectApril30() -> None:
   assert KIDS.end_for( True, NOVEMBER ) == date( 2027, 4, 30 )


def Test_EndFor_TestWindowSoonerThanTwoWeeks_ExpectTwoWeeks() -> None:
   assert CANADIAN.end_for( False, date( 2026, 11, 20 ) ) == date( 2026, 12, 4 )


def Test_ClosedUntilMonth_TestJanuaryOpening_ExpectDecember() -> None:
   assert ExhibitSeason( 1, 3 ).closed_until_month() == 12


def Test_EndFor_TestOpenPastTheWindow_ExpectTwoWeeks() -> None:
   assert CANADIAN.end_for( False, date( 2026, 12, 1 ) ) == date( 2026, 12, 15 )


def Test_EndFor_TestClosedInsideTheOpenSeason_ExpectTwoWeeks() -> None:
   assert MAYAN.end_for( True, date( 2026, 6, 1 ) ) == date( 2026, 6, 15 )


def Test_InOpenSeason_TestNoMonths_ExpectClosed() -> None:
   assert ExhibitSeason().in_open_season( NOVEMBER ) is False


def Test_ClosedUntilMonth_TestNoMonths_ExpectNone() -> None:
   assert ExhibitSeason().closed_until_month() is None


def Test_EndFor_TestNoMonths_ExpectTwoWeeks() -> None:
   assert ExhibitSeason().end_for( True, NOVEMBER ) == date( 2026, 11, 25 )
   assert ExhibitSeason().end_for( False, NOVEMBER ) == date( 2026, 11, 25 )
