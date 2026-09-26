from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import DateValues
from api.shared.opening_schedule_date_resolver import OpeningScheduleDateResolver


def Test_ParseEndDate_TestMissingEndDate_ExpectMaxDate() -> None:
   value = None

   parsed = OpeningScheduleDateResolver.parse_end_date( value )

   assert parsed == date.max


def Test_ParseEndDate_TestExplicitDate_ExpectParsedDate() -> None:
   value = '2026-06-30'

   parsed = OpeningScheduleDateResolver.parse_end_date( value )

   assert parsed == DateValues.parse_date_value( value )


def Test_FormatDate_TestMaxDate_ExpectNone() -> None:
   value = date.max

   formatted = OpeningScheduleDateResolver.format_date( value )

   assert formatted is None


def Test_FormatDate_TestConcreteDate_ExpectIsoDateKey() -> None:
   value = date( 2026, 6, 15 )

   formatted = OpeningScheduleDateResolver.format_date( value )

   assert formatted == value.isoformat()
