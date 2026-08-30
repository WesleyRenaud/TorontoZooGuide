from __future__ import annotations

from datetime import date

from api.shared.opening_schedule_date_resolver import OpeningScheduleDateResolver


def Test_ParseEndDate_TestMissingEndDate_ExpectMaxDate() -> None:
   assert OpeningScheduleDateResolver.parse_end_date( None ) == date.max


def Test_ParseEndDate_TestExplicitDate_ExpectParsedDate() -> None:
   assert OpeningScheduleDateResolver.parse_end_date( '2026-06-30' ) == date( 2026, 6, 30 )


def Test_FormatDate_TestMaxDate_ExpectNone() -> None:
   assert OpeningScheduleDateResolver.format_date( date.max ) is None


def Test_FormatDate_TestConcreteDate_ExpectIsoDateKey() -> None:
   assert OpeningScheduleDateResolver.format_date( date( 2026, 6, 15 ) ) == '2026-06-15'
