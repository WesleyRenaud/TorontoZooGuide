from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import datetime
from typing import Any

import pytest

import api.shared.calendar_dates as calendar_dates
from api.shared.calendar_dates import CalendarDates
from api.shared.calendar_dates import DateValues
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
def test_normalize_month( value: Types.MonthInput, expected: Types.VisitMonth | None ) -> None:
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
def test_get_month_abbreviation( value: Types.MonthInput, expected: str ) -> None:
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
      value: Types.MonthInput,
      expected: Types.VisitMonth ) -> None:
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
def test_is_peak_season_month( month: Types.MonthInput, expected: bool ) -> None:
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


def test_next_weekday_date_advances_from_weekend() -> None:
   assert CalendarDates.next_weekday_date( date( 2026, 6, 20 ) ) == date( 2026, 6, 22 )
   assert CalendarDates.next_weekday_date( date( 2026, 6, 15 ) ) == date( 2026, 6, 15 )


def test_next_weekend_or_holiday_date_advances_from_weekday() -> None:
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 6, 15 ) ) == date( 2026, 6, 20 )
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 6, 20 ) ) == date( 2026, 6, 20 )
   assert CalendarDates.next_weekend_or_holiday_date(
      date( 2026, 7, 1 ) ) == date( 2026, 7, 1 )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( date( 2026, 6, 15 ), date( 2026, 6, 15 ) ),
      ( datetime( 2026, 6, 15, 9, 30 ), date( 2026, 6, 15 ) ),
      ( '2026-06-15', date( 2026, 6, 15 ) ),
      ( '2026-06-15 09:30', date( 2026, 6, 15 ) )
   ]
)
def test_parse_date_value( value: Types.DateInput, expected: date | None ) -> None:
   assert DateValues.parse_date_value( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '  ', None ),
      ( '2026-06-15', '2026-06-15' ),
      ( date( 2026, 6, 15 ), '2026-06-15' ),
      ( datetime( 2026, 6, 15, 9, 30 ), '2026-06-15' ),
   ]
)
def test_normalize_date_key( value: Types.DateInput, expected: Types.DateKey | None ) -> None:
   assert DateValues.normalize_date_key( value ) == expected


def test_normalize_date_key_returns_none_for_unsupported_date_strings() -> None:
   assert DateValues.normalize_date_key( 'June 15, 2026' ) is None


def test_resolve_open_ended_date_range_keeps_open_end_date() -> None:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date='2026-06-01',
      end_date=None )

   assert date_range.start_date == '2026-06-01'
   assert date_range.end_date is None


def test_resolve_open_ended_date_range_uses_today_for_missing_start(
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   date_range = DateValues.resolve_open_ended_date_range(
      start_date=None,
      end_date=None )

   assert date_range.start_date == '2026-06-15'
   assert date_range.end_date is None


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '2026-06-15 09:30 AM', datetime( 2026, 6, 15, 9, 30 ) ),
      ( '2026-06-15 17:45:00', datetime( 2026, 6, 15, 17, 45 ) ),
      ( '2026-06-15 17:45', datetime( 2026, 6, 15, 17, 45 ) )
   ]
)
def test_parse_datetime_value( value: str | None, expected: datetime | None ) -> None:
   assert DateValues.parse_datetime_value( value ) == expected


def test_parse_values_raise_for_unsupported_formats() -> None:
   with pytest.raises( ValueError ):
      DateValues.parse_date_value( 'June 15, 2026' )

   with pytest.raises( ValueError ):
      DateValues.parse_datetime_value( 'June 15, 2026 9:30' )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '   ', None ),
      ( '1:00 PM', '1:00 PM' ),
      ( '13:45', '1:45 PM' ),
      ( '13:45:30', '1:45:30 PM' ),
      ( '10:00', '10:00 AM' ),
      ( 'not-a-time', None ),
   ]
)
def test_normalize_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   assert DateValues.normalize_schedule_time( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '   ', None ),
      ( '1:00 PM', '1:00 PM' ),
      ( '13:45', '1:45 PM' ),
      ( '13:45:30', '1:45:30 PM' ),
      ( '10:00', '10:00 AM' ),
      ( 'not-a-time', None ),
   ]
)
def test_normalize_itinerary_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   assert DateValues.normalize_itinerary_schedule_time( value ) == expected


@pytest.mark.parametrize(
   'values, expected',
   [
      ( [], [] ),
      ( [ '2:00 PM', '3:30 PM' ], [ '2:00 PM', '3:30 PM' ] ),
      ( [ '3:30 PM', '15:30', '2:00 PM' ], [ '3:30 PM', '2:00 PM' ] ),
      ( [ '1:00 PM', 'not-a-time', '13:00' ], [ '1:00 PM' ] ),
   ]
)
def test_normalize_unique_schedule_times(
      values: list[ str ],
      expected: list[ str ] ) -> None:
   assert DateValues.normalize_unique_schedule_times( values ) == expected

@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, '' ),
      ( '', '' ),
      ( '   ', '' ),
      ( '09:30', '09:30' ),
      ( ' 1:00 PM ', '1:00 PM' ),
   ]
)
def test_normalize_schedule_time_key(
      value: str | None,
      expected: str ) -> None:
   assert DateValues.normalize_schedule_time_key( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '09:30', 9 * 3600 + 30 * 60 ),
      ( '09:30:30', 9 * 3600 + 30 * 60 + 30 ),
      ( '1:00 PM', 13 * 3600 ),
   ]
)
def test_time_value_in_seconds(
      value: str | None,
      expected: int | None ) -> None:
   assert DateValues.time_value_in_seconds( value ) == expected


def test_time_value_is_at_or_after() -> None:
   assert DateValues.time_value_is_at_or_after( '10:30 AM', '10:30 AM' )
   assert DateValues.time_value_is_at_or_after( '10:30 AM', '10:15 AM' )
   assert not DateValues.time_value_is_at_or_after( '10:15 AM', '10:30 AM' )
   assert not DateValues.time_value_is_at_or_after( None, '10:30 AM' )
   assert not DateValues.time_value_is_at_or_after( '10:30 AM', None )


@pytest.mark.parametrize(
   'total_seconds, expected',
   [
      ( 9 * 3600 + 30 * 60, '9:30 AM' ),
      ( 9 * 3600 + 30 * 60 + 30, '9:30:30 AM' ),
   ]
)
def test_schedule_time_key_from_seconds(
      total_seconds: int,
      expected: str ) -> None:
   assert DateValues.schedule_time_key_from_seconds( total_seconds ) == expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', False ),
      ( date( 2026, 6, 16 ), '2026-06-14', True ),
   ]
)
def test_is_date_on_or_after( left: date, right: Types.DateInput, expected: bool ) -> None:
   assert DateValues.is_date_on_or_after( left, right ) is expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 16 ), '2026-06-15', False ),
      ( date( 2026, 6, 14 ), '2026-06-14', True ),
   ]
)
def test_is_date_on_or_before( left: date, right: Types.DateInput, expected: bool ) -> None:
   assert DateValues.is_date_on_or_before( left, right ) is expected


@pytest.mark.parametrize(
   'target, start, end, expected',
   [
      ( date( 2026, 6, 15 ), None, None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', None, False ),
      ( date( 2026, 6, 16 ), None, '2026-06-15', False )
   ]
)
def test_is_date_in_range(
      target: date,
      start: Types.DateInput,
      end: Types.DateInput,
      expected: bool ) -> None:
   assert DateValues.is_date_in_range( target_date=target, start_date_value=start, end_date_value=end ) is expected
