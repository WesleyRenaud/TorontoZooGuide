from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Any

import pytest

from api.shared.calendar_dates import CalendarDates
import api.shared.date_values as date_values
from api.types import Types


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
def Test_normalize_month( value: Types.MonthInput, expected: Types.VisitMonth | None ) -> None:
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
def Test_get_month_abbreviation( value: Types.MonthInput, expected: str ) -> None:
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
def Test_get_month_abbreviation_rejects_invalid_values( value: Any ) -> None:
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
def Test_resolve_visit_calendar_month(
      value: Types.MonthInput,
      expected: Types.VisitMonth ) -> None:
   got = CalendarDates.resolve_visit_calendar_month( value )
   assert got == expected
   assert isinstance( got, int )


def Test_ResolveVisitCalendarMonth_TestInvalidValues_ExpectRaises() -> None:
   with pytest.raises( ValueError ):
      CalendarDates.resolve_visit_calendar_month( 13 )


def Test_ResolveVisitDayOfMonth_TestValidValues_ExpectDayNumber() -> None:
   assert CalendarDates.resolve_visit_day_of_month( '15' ) == 15
   assert CalendarDates.resolve_visit_day_of_month( 7 ) == 7


def Test_ResolveVisitCalendarYear_TestExplicitYear_ExpectValue() -> None:
   assert CalendarDates.resolve_visit_calendar_year( 2029 ) == 2029


def Test_ResolveVisitCalendarYear_TestNone_ExpectModuleDatetime( monkeypatch: pytest.MonkeyPatch ) -> None:
   class Fixed( datetime ):
      @classmethod
      def now( cls, tz: datetime.tzinfo | None = None ) -> datetime:
         return datetime( 2032, 3, 1, 0, 0, 0 )

   monkeypatch.setattr( date_values, 'datetime', Fixed )
   assert CalendarDates.resolve_visit_calendar_year( None ) == 2032


def Test_VisitTargetDate_TestValidInputs_ExpectDate() -> None:
   assert CalendarDates.visit_target_date( 'June', 15, 2026 ) == date( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 6, 15, 2026 ) == date( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 'January', 10, '2028' ) == date( 2028, 1, 10 )


def Test_ScheduleIncludesWeekday_TestMondayFirst_ExpectTrue() -> None:
   flags = ( True, False, False, False, False, False, False )

   assert CalendarDates.schedule_includes_weekday( 0, flags ) is True
   assert CalendarDates.schedule_includes_weekday( 1, flags ) is False


def Test_ScheduleIncludesWeekday_TestBadIndex_ExpectRaises() -> None:
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
def Test_get_day_of_year( month: str, day: int, expected: int ) -> None:
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
def Test_get_next_month( month: str, expected: str | None ) -> None:
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
def Test_get_number_of_days_in_month( month: str, expected: int | None ) -> None:
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
def Test_is_peak_season_month( month: Types.MonthInput, expected: bool ) -> None:
   assert CalendarDates.is_peak_season_month( month ) is expected


def Test_GetEasterDate_TestYear2026_ExpectAprilFifth() -> None:
   assert CalendarDates.get_easter_date( 2026 ) == date( 2026, 4, 5 )


def Test_GetCanadianHolidays_TestYear2026_ExpectExpectedDates() -> None:
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
def Test_is_holiday_recognizes_canadian_holidays( holiday: date ) -> None:
   assert CalendarDates.is_holiday( holiday ) is True


def Test_IsHoliday_TestRegularDays_ExpectFalse() -> None:
   assert CalendarDates.is_holiday( date( 2026, 12, 24 ) ) is False
   assert CalendarDates.is_holiday( date( 2026, 6, 15 ) ) is False


def Test_NextWeekdayDate_TestFromWeekend_ExpectMonday() -> None:
   assert CalendarDates.next_weekday_date( date( 2026, 6, 20 ) ) == date( 2026, 6, 22 )
   assert CalendarDates.next_weekday_date( date( 2026, 6, 15 ) ) == date( 2026, 6, 15 )


def Test_NextWeekendOrHolidayDate_TestFromWeekday_ExpectSaturday() -> None:
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 6, 15 ) ) == date( 2026, 6, 20 )
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 6, 20 ) ) == date( 2026, 6, 20 )
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 7, 1 ) ) == date( 2026, 7, 1 )


def Test_ResolveVisitCalendarMonth_TestNormalizeReturnsNone_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      CalendarDates,
      'normalize_month',
      lambda **kwargs: None )

   with pytest.raises( ValueError, match='Invalid month' ):
      CalendarDates.resolve_visit_calendar_month( 'June' )
