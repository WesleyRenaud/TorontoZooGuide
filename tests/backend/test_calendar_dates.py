from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Any

import pytest

from api.shared.calendar_dates import CalendarDates
import api.shared.date_values as date_values
from api.types import MonthInput
from api.types import VisitMonth


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( 1, 1 ),
      ( 12, 12 ),
      ( 0, None ),
      ( 13, None ),
      ( '1', None ),
      ( 'January', 1 ),
      ( 'Jan', 1 ),
      ( 'JAN', 1 ),
      ( 'February', 2 ),
      ( 'Feb', 2 ),
      ( 'FEB', 2 ),
      ( 'March', 3 ),
      ( 'Mar', 3 ),
      ( 'MAR', 3 ),
      ( 'April', 4 ),
      ( 'Apr', 4 ),
      ( 'APR', 4 ),
      ( 'May', 5 ),
      ( 'MAY', 5 ),
      ( 'June', 6 ),
      ( 'Jun', 6 ),
      ( 'JUN', 6 ),
      ( 'July', 7 ),
      ( 'Jul', 7 ),
      ( 'JUL', 7 ),
      ( 'August', 8 ),
      ( 'Aug', 8 ),
      ( 'AUG', 8 ),
      ( 'September', 9 ),
      ( 'Sep', 9 ),
      ( 'SEP', 9 ),
      ( 'October', 10 ),
      ( 'Oct', 10 ),
      ( 'OCT', 10 ),
      ( 'November', 11 ),
      ( 'Nov', 11 ),
      ( 'NOV', 11 ),
      ( 'December', 12 ),
      ( 'Dec', 12 ),
      ( 'DEC', 12 ),
      ( 'december', None ),
      ( 'NotAMonth', None ),
   ]
)
def test_normalize_month( value: MonthInput, expected: VisitMonth | None ) -> None:
   assert CalendarDates.normalize_month( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 'Jan' ),
      ( 12, 'Dec' ),
      ( '1', 'Jan' ),
      ( '12', 'Dec' ),
      ( 'January', 'Jan' ),
      ( 'sept', 'Sep' ),
      ( 'DECEMBER', 'Dec' ),
   ]
)
def test_get_month_abbreviation( value: MonthInput, expected: str ) -> None:
   assert CalendarDates.get_month_abbreviation( value ) == expected


@pytest.mark.parametrize(
   'value',
   [
      0,
      13,
      '13',
      'NotAMonth',
      [],
   ]
)
def test_get_month_abbreviation_rejects_invalid_values( value: Any ) -> None:
   with pytest.raises( ValueError ):
      CalendarDates.get_month_abbreviation( value )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 1 ),
      ( 6, 6 ),
      ( '06', 6 ),
      ( 'June', 6 ),
      ( 'JUN', 6 ),
      ( 'January', 1 ),
      ( 'december', 12 ),
   ]
)
def test_resolve_visit_calendar_month(
      value: MonthInput,
      expected: VisitMonth ) -> None:
   got = CalendarDates.resolve_visit_calendar_month( value )
   assert got == expected
   assert isinstance( got, int )


def test_resolve_visit_calendar_month_rejects_invalid_values() -> None:
   with pytest.raises( ValueError ):
      CalendarDates.resolve_visit_calendar_month( 13 )


def test_resolve_visit_day_of_month() -> None:
   assert CalendarDates.resolve_visit_day_of_month( '15' ) == 15
   assert CalendarDates.resolve_visit_day_of_month( 7 ) == 7


def test_resolve_visit_calendar_year_explicit() -> None:
   assert CalendarDates.resolve_visit_calendar_year( 2029 ) == 2029


def test_resolve_visit_calendar_year_none_uses_module_datetime( monkeypatch: pytest.MonkeyPatch ) -> None:
   class Fixed( datetime ):
      @classmethod
      def now( cls, tz: datetime.tzinfo | None = None ) -> datetime:
         return datetime( 2032, 3, 1, 0, 0, 0 )

   monkeypatch.setattr( date_values, 'datetime', Fixed )
   assert CalendarDates.resolve_visit_calendar_year( None ) == 2032


def test_visit_target_date() -> None:
   assert CalendarDates.visit_target_date( 'June', 15, 2026 ) == date( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 6, 15, 2026 ) == date( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 'January', 10, '2028' ) == date( 2028, 1, 10 )


def test_schedule_includes_weekday_monday_first() -> None:
   flags = ( True, False, False, False, False, False, False )

   assert CalendarDates.schedule_includes_weekday( 0, flags ) is True
   assert CalendarDates.schedule_includes_weekday( 1, flags ) is False


def test_schedule_includes_weekday_rejects_bad_index() -> None:
   flags = ( True, ) * 7

   assert CalendarDates.schedule_includes_weekday( -1, flags ) is False
   assert CalendarDates.schedule_includes_weekday( 7, flags ) is False


@pytest.mark.parametrize(
   'month, day, expected',
   [
      ( 'JAN', 1, 0 ),
      ( 'FEB', 1, 31 ),
      ( 'MAR', 1, 59 ),
      ( 'APR', 15, 104 ),
      ( 'JUN', 15, 165 ),
      ( 'DEC', 31, 364 ),
   ]
)
def test_get_day_of_year( month: str, day: int, expected: int ) -> None:
   assert CalendarDates.get_day_of_year( month, day ) == expected


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 'Jan', 'Feb' ),
      ( 'JAN', 'Feb' ),
      ( 'Feb', 'Mar' ),
      ( 'MAR', 'Apr' ),
      ( 'Apr', 'May' ),
      ( 'MAY', 'Jun' ),
      ( 'Jun', 'Jul' ),
      ( 'JUL', 'Aug' ),
      ( 'Aug', 'Sep' ),
      ( 'SEP', 'Oct' ),
      ( 'Oct', 'Nov' ),
      ( 'NOV', 'Dec' ),
      ( 'Dec', 'Jan' ),
      ( 'DEC', 'Jan' ),
      ( 'BadMonth', None ),
   ]
)
def test_get_next_month( month: str, expected: str | None ) -> None:
   assert CalendarDates.get_next_month( month ) == expected


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 'JAN', 31 ),
      ( 'Jan', 31 ),
      ( 'MAR', 31 ),
      ( 'APR', 30 ),
      ( 'Apr', 30 ),
      ( 'JUN', 30 ),
      ( 'SEP', 30 ),
      ( 'NOV', 30 ),
      ( 'FEB', 28 ),
      ( 'Feb', 28 ),
      ( 'BadMonth', None ),
   ]
)
def test_get_number_of_days_in_month( month: str, expected: int | None ) -> None:
   assert CalendarDates.get_number_of_days_in_month( month ) == expected


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 5, True ),
      ( 6, True ),
      ( 10, True ),
      ( 'May', True ),
      ( 'October', True ),
      ( 4, False ),
      ( 11, False ),
      ( 'April', False ),
      ( 'November', False ),
   ]
)
def test_is_peak_season_month( month: MonthInput, expected: bool ) -> None:
   assert CalendarDates.is_peak_season_month( month ) is expected


def test_get_easter_date() -> None:
   assert CalendarDates.get_easter_date( 2026 ) == date( 2026, 4, 5 )


def test_canadian_holiday_dates_for_2026() -> None:
   assert CalendarDates.get_family_day( 2026 ) == date( 2026, 2, 16 )
   assert CalendarDates.get_good_friday( 2026 ) == date( 2026, 4, 3 )
   assert CalendarDates.get_victoria_day( 2026 ) == date( 2026, 5, 18 )
   assert CalendarDates.get_civic_holiday( 2026 ) == date( 2026, 8, 3 )
   assert CalendarDates.get_labour_day( 2026 ) == date( 2026, 9, 7 )
   assert CalendarDates.get_thanksgiving( 2026 ) == date( 2026, 10, 12 )


@pytest.mark.parametrize(
   'holiday',
   [
      date( 2026, 1, 1 ),
      date( 2026, 2, 16 ),
      date( 2026, 4, 3 ),
      date( 2026, 5, 18 ),
      date( 2026, 7, 1 ),
      date( 2026, 8, 3 ),
      date( 2026, 9, 7 ),
      date( 2026, 10, 12 ),
      date( 2026, 12, 25 ),
   ]
)
def test_is_holiday_recognizes_canadian_holidays( holiday: date ) -> None:
   assert CalendarDates.is_holiday( holiday ) is True


def test_is_holiday_rejects_regular_days() -> None:
   assert CalendarDates.is_holiday( date( 2026, 12, 24 ) ) is False
   assert CalendarDates.is_holiday( date( 2026, 6, 15 ) ) is False
